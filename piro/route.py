import logging

import numpy as np
import plotly.express as px
import pandas as pd
import os
import json

from pymatgen.core import Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram
from pymatgen.util.string import latexify
from tqdm import tqdm

from piro.data import GASES, GAS_RELEASE, DEFAULT_GAS_PRESSURES
from piro.mprester import get_mprester
from piro.reactions import get_reactions
from piro.settings import CacheType, settings
from piro.utils import get_epitaxies, get_similarities


logger = logging.getLogger(__name__)


class SynthesisRoutes:
    def __init__(
        self,
        target_entry_id,
        confine_to_icsd=True,
        confine_to_stables=True,
        hull_distance=None,
        simple_precursors=False,
        explicit_includes=None,
        exclude_compositions=None,
        allow_gas_release=False,
        add_elements=None,
        flexible_competition=0,
        entries=None,
        epitaxies=None,
        similarities=None,
        sigma=2 * 6.242 * 0.01,
        transport_constant=10.0,
        custom_target_entry=None,
        confine_competing_to_icsd=False
    ):
        """
        Synthesis reaction route recommendations, derived semi-empirically using the Classical Nucleation Theory
            and high-throughput DFT data (doi: 10.1021/jacs.1c04888). After instantiation, synthesis planning plots
            are generated using the recommend_routes method (See this method's arguments as well).
            Precursor library, epitaxial match and similarity metrics are precomputed upon instantiation,
            and can be cached.

        Args:
            target_entry_id (str): Materials Project entry id for target material
            confine_to_icsd (bool): Use ICSD-sourced entries to find precursors. Defaults to True.
            confine_to_stables (bool): Use stable entries only to find. Defaults to True.
            hull_distance (float): Use entries within this distance to hull (eV/atom). Can significantly increase
                number of possible precursors and slow down the predictions. Ignored if confine_to_stables is True.
            simple_precursors (bool or int): If True, or integer >0, precursors with fewer components will
                be considered. Defaults to False.
            explicit_includes (list): list of MP-ids to explicitly include. For example, confine_to_stables may exclude
                certain common precursors in some systems, if they are not on the convex-hull - this allows such
                potential precursors to be added to the library manually.
            exclude_compositions (list): list of compositions to avoid in precursor library. All entries at this
                composition are removed from the precursor library.
            allow_gas_release (bool): Many reactions require the release of gases like CO2, O2, etc. depending on the
                precursors, which requires explicitly considering them in balancing the reactions. Defaults to False.
            add_elements List(str): Add elements to the chemical space of libraries that doesn't exist in the target
                material. Best example is 'C', which would allow carbonates to be added to the precursor library.
            flexible_competition (int): This parameter specifies the depth of the competing phase search, and can help
                add more resolution to the phase competition axis of the recommendation plot.
                Defaults to 0, which would include only competing phases that have the same number of elements as the
                target. A reliable heuristic is setting it as 1, if x-axis of the plot is not informative.
            entries (list): List of Materials Project ComputedEntry objects, as can be obtained via the API. If provided
                these entries will be used while forming the precursor library. If not provided, MP database will be
                queried via their Rest API to get the most up-to-date entries. Defaults to None.
            epitaxies (dict): Dict of minimum matching areas between the target and entries, normally as computed
                via the get_epitaxies method. Recommended use is to leave as None.
            similarities (dict): Dict of similarity quantiles between the target and entries, normally as computed
                via the get_similarities method. Recommended use is to leave as None.
            sigma (float): surface energy constant (eV/Ang^2) to be used in predictions. Defaults to equivalent of
                2.0 J/m^2.
            transport_constant (float): diffusion barrier coefficient (max barrier). Defaults to 10.0 eV.
            custom_target_entry (MP entry): custom ComputedEntry pymatgen object. It can be used to plan synthesis
                of a user-supplied compound that does not have a corresponding MP entry.
            allow_gas_release (bool): Many reactions require the release of gases like CO2, O2, etc. depending on the
                precursors, which requires explicitly considering them in balancing the reactions. Defaults to False.
            confine_competing_to_icsd (bool): Use ICSD-sourced entries to as competing compounds. Defaults to False.
        """

        self.target_entry_id = target_entry_id
        self.confine_to_icsd = confine_to_icsd
        self.confine_to_stables = confine_to_stables
        self.simple_precursors = simple_precursors
        self.explicit_includes = explicit_includes if explicit_includes else []
        self.allow_gas_release = allow_gas_release
        self.temperature = None
        self.pressure = None
        self.add_elements = add_elements if add_elements else []
        self.entries = entries
        self.hull_distance = hull_distance
        self.confine_competing_to_icsd = confine_competing_to_icsd
        self.exclude_compositions = exclude_compositions
        self.custom_target_entry = custom_target_entry
        self.flexible_competition = flexible_competition if flexible_competition is not None else 0
        self._sigma = sigma if sigma is not None else 2 * 6.242 * 0.01
        self._transport_constant = transport_constant if transport_constant is not None else 10.0

        self.plot_data = None
        self.reactions = {}
        if not entries:
            if not custom_target_entry:
                with get_mprester() as mpr:
                    _e = mpr.get_entry_by_material_id(self.target_entry_id)
                    if isinstance(_e, list):
                        _e = _e[0]
            else:
                _e = custom_target_entry
            self.elts = list(_e.composition.as_dict().keys())
            if add_elements:
                self.elts.extend(add_elements)
            self.get_mp_entries()
        else:
            self.elts = list(self.target_entry.composition.as_dict().keys())

        self.get_precursor_library()
        print("Precursor library ready.")
        cache_type = CacheType.NO_CACHE if self.custom_target_entry else settings.cache_type
        print("Epitaxy and Similarity cache type: ", cache_type)
        self.epitaxies = epitaxies if epitaxies else get_epitaxies(
            self.precursor_library,
            self.target_entry,
            cache_type
        )
        self.similarities = similarities if similarities else get_similarities(
            self.precursor_library,
            self.target_entry,
            cache_type
        )

        self._reactions_objs = None

    @property
    def reactions_objs(self):
        if not self._reactions_objs:
            self._reactions_objs = get_reactions(
                self.target_entry,
                self.elts,
                self.precursor_library,
                self.allow_gas_release
            )
            logger.info(f"Total # of balanced reactions obtained: {len(self.reactions_objs)}")
        return self._reactions_objs

    def get_mp_entries(self):
        with get_mprester() as mpr:
            if len(mpr.api_key) == 32:
                self.entries = mpr.get_entries_in_chemsys(
                    self.elts,
                    inc_structure="final",
                    property_data=["material_id", "formation_energy_per_atom"],
                )
                # Hack to fix MP append
                for entry in self.entries:
                    entry.entry_id = entry.entry_id.replace("-GGA", "")
                mp_ids = [ent.data['material_id'] for ent in self.entries]
                provs = mpr.provenance.search(mp_ids, fields=['material_id', 'database_IDs', 'theoretical'])
                from emmet.core.provenance import Database
                mp_to_icsd = {str(doc.material_id): doc.database_IDs.get(Database.ICSD)
                              for doc in provs if not doc.theoretical}
                for entry in self.entries:
                    entry.data.update({"icsd_ids": mp_to_icsd.get(entry.data['material_id'])})
            else:
                self.entries = mpr.get_entries_in_chemsys(
                    self.elts,
                    inc_structure="final",
                    property_data=["icsd_ids", "formation_energy_per_atom"],
                )
        for entry in self.entries:
            entry.structure.entry_id = entry.entry_id
        print("Total # of entries found in this chemistry: ", len(self.entries))

    @property
    def target_entry(self):
        if self.custom_target_entry:
            return self.custom_target_entry
        else:
            return [e for e in self.entries if e.entry_id == self.target_entry_id][0]

    def get_precursor_library(self):
        phased = PhaseDiagram(self.entries)
        if self.confine_to_stables:
            precursor_library = list(phased.stable_entries)
        elif self.hull_distance is not None:
            precursor_library = [
                e
                for e in self.entries
                if phased.get_e_above_hull(e) <= self.hull_distance
            ]
        else:
            precursor_library = [e for e in self.entries]

        if self.confine_to_icsd:
            precursor_library = [i for i in precursor_library if i.data["icsd_ids"]]

        if self.simple_precursors:
            precursor_library = [
                i
                for i in precursor_library
                if len(i.composition.elements)
                < len(self.target_entry.composition.elements)
                - self.simple_precursors
                + 1
            ]

        if self.target_entry in precursor_library:
            precursor_library.pop(precursor_library.index(self.target_entry))

        if self.explicit_includes:
            print("explicitly including: ", self.explicit_includes)
            for entry_id in self.explicit_includes:
                try:
                    entry = [e for e in self.entries if e.entry_id == entry_id][0]
                except IndexError:
                    print("Could not find {} in entry list".format(entry_id))
                    continue
                if entry not in precursor_library:
                    precursor_library.append(entry)

        if self.exclude_compositions:
            precursor_library = [
                i
                for i in precursor_library
                if i.composition.reduced_formula not in self.exclude_compositions
            ]

        self.precursor_library = precursor_library

        print(
            "Total # of precursors materials obeying the provided filters: ",
            len(precursor_library),
        )
        return self.precursor_library

    @property
    def sigma(self):
        return self._sigma

    @property
    def transport_constant(self):
        return self._transport_constant

    def get_reactions_with_energies(self):
        reactions_dict = {}
        for r in tqdm(
            self.reactions_objs,
            desc='Calculating reaction results',
            total=len(self._reactions_objs)
        ):
            if r.label in reactions_dict:
                continue
            else:
                r.update_reaction_energy(
                    self.temperature,
                    self.pressure
                )
                r.update_nucleation_barrier(
                    self.epitaxies,
                    self.similarities,
                    self.sigma,
                    self.transport_constant
                )
                r.update_reaction_summary()
                r.update_competing_phases(
                    self.entries,
                    self.confine_competing_to_icsd,
                    self.flexible_competition,
                    self.allow_gas_release,
                    self.temperature,
                    self.pressure
                )
                reactions_dict[r.label] = r.as_dict()

        return reactions_dict

    def recommend_routes(
        self,
        temperature=298.0,
        pressure=DEFAULT_GAS_PRESSURES,
        max_component_precursors=0,
        show_fraction_known_precursors=True,
        show_known_precursors_only=False,
        display_peroxides=True,
        display_superoxides=True,
        w=None,
        h=None,
        xrange=None,
        yrange=None,
        add_pareto=False,
        custom_text="",
    ):
        """
        Synthesis reaction route recommendations, derived semi-empirically using the Classical Nucleation Theory
            and high-throughput DFT data (doi: 10.1021/jacs.1c04888). After instantiation, synthesis planning plots
            are generated using this method.
        Args:
            temperature (float): Temperature (in Kelvin) to consider in free energy adjustments for gases.
            pressure (dict or float): Gas pressures (in atm). If float, all gases are assumed to have the same constant
                pressure. A dictionary in the form of {'O2': 0.21, 'CO2':, 0.05} can be provided to explicitly
                specify partial pressures. Defaults to a default pressure dictionary pertaining to
                open atmosphere conditions.
            max_component_precursors (int): Used to limit the reactants to simpler sub-chemistries of our target to
                obtain a more refined candidate precursor list. If set, compounds with more unique elements than this
                limit are ignored as precursors. For example, for a ternary target compound, max_component_precursors=2
                would limit precursors to binary compounds (add_element is ignored, i.e. carbonated versions of binary
                compounds would also be included).
            show_known_precursors_only (bool): applies an additional filter to the precursor list during reaction
                generation to select only those phases text-mined by Kononova et al. (doi: 10.1038/s41597-019-0224-1)
                as solid-state precursors. Defaults to False.
            show_fraction_known_precursors (bool): can color-code the reactions based on what fraction of the precursors
                are in the above text-mined dataset. Defaults to True.
            display_peroxides (bool): whether reactions involving peroxides are included in the plot. Defaults to True.
            display_superoxides (bool): whether reactions involving superoxides are included in the plot.
                Defaults to True.
            w (int): width of the generated plot in pixels
            h (int): height of the generated plot in pixels
            xrange (tuple): sets the x-axis range
            yrange (tuple): sets the y-axis range
            add_pareto (bool): adds the Pareto front line to the plot.
            custom_text (str): text appended to the figure title.
        """
        if not (self.pressure == pressure and self.temperature == temperature):
            self.temperature = temperature if temperature is not None else 298.0
            self.pressure = pressure if pressure is not None else DEFAULT_GAS_PRESSURES
            self.reactions = self.get_reactions_with_energies()

        self.check_if_known_precursors()

        self.plot_data = pd.DataFrame.from_dict(self.reactions, orient="index")[
            [
                "n_competing",
                "barrier",
                "summary",
                "energy",
                "enthalpy",
                "exp_precursors",
                "precursor_formulas",
            ]
        ]
        if max_component_precursors:
            allowed_precursor_ids = [
                i.entry_id
                for i in self.precursor_library
                if len(set(i.composition.as_dict().keys()).difference(self.add_elements))
                <= max_component_precursors
                or i.composition.reduced_formula in GAS_RELEASE
            ]
            display_reactions = []
            for r in self.plot_data.index.to_list():
                if set(r.split("_")).issubset(set(allowed_precursor_ids)):
                    display_reactions.append(r)
            self.plot_data = self.plot_data.loc[display_reactions]

        if not display_peroxides:
            peroxides = {
                "Li2O2",
                "K2O2",
                "BaO2",
                "Rb2O2",
                "Cs2O2",
                "Na2O2",
                "SrO2",
                "CaO2",
                "MgO2",
                "ZnO2",
                "CdO2",
                "HgO2",
            }
            allowed_rows = []
            for i in range(len(self.plot_data)):
                if not peroxides.intersection(
                    set(self.plot_data["precursor_formulas"][i].tolist())
                ):
                    allowed_rows.append((i))
            self.plot_data = self.plot_data.iloc[allowed_rows]

        if not display_superoxides:
            superoxides = {"LiO2", "NaO2", "KO2", "RbO2", "CsO2"}
            allowed_rows = []
            for i in range(len(self.plot_data)):
                if not superoxides.intersection(
                    set(self.plot_data["precursor_formulas"][i].tolist())
                ):
                    allowed_rows.append((i))
            self.plot_data = self.plot_data.iloc[allowed_rows]

        color = "exp_precursors" if show_fraction_known_precursors else None

        if show_known_precursors_only:
            self.plot_data = self.plot_data[
                self.plot_data["exp_precursors"].astype(float) == 1.0
            ]
        fig = px.scatter(
            self.plot_data,
            x="n_competing",
            y="barrier",
            hover_data=["summary"],
            color=color,
            width=w,
            height=h,
            template="simple_white",
        )
        for i in fig.data:
            i.marker.size = 10
        fig.update_layout(
            yaxis={
                "title": "Nucleation barrier (a.u.)",
                "ticks": "inside",
                "mirror": True,
                "showline": True,
            },
            xaxis={
                "title": "Number of competing phases",
                "ticks": "inside",
                "mirror": True,
                "showline": True,
            },
            font={"size": 13},
            title=r"Target: "
            + self.target_entry.structure.composition.reduced_formula
            + custom_text,
            title_font_size=15,
            title_x=0.5,
        )
        fig.update_traces(
            marker=dict(
                size=12, line=dict(width=2, color="DarkSlateGrey"), opacity=0.8
            ),
            selector=dict(mode="markers"),
        )
        if xrange:
            fig.update_xaxes(range=xrange)
        if yrange:
            fig.update_yaxes(range=yrange)

        if add_pareto:
            import plotly.graph_objects as go

            _pareto_data = self.topsis().loc[self.get_pareto_front()]
            _x = _pareto_data["n_competing"]
            _y = _pareto_data["barrier"]
            fig.add_trace(
                go.Scatter(
                    x=_x,
                    y=_y,
                    line=dict(color="firebrick", width=2),
                    hoverinfo='skip'
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[_x[0], _x[0], None, _x[-1], self.topsis()["n_competing"].max()],
                    y=[_y[0], self.topsis()["barrier"].max(), None, _y[-1], _y[-1]],
                    line=dict(color="firebrick", width=2, dash="dash"),
                    connectgaps=False,
                    hoverinfo='skip'
                )
            )

            fig.update_layout(showlegend=False)
        return fig

    def get_precursor_formulas(self, include_ids=True):
        if include_ids:
            return [
                (p.entry_id, p.composition.reduced_formula)
                for p in self.precursor_library
            ]
        else:
            return [p.composition.reduced_formula for p in self.precursor_library]

    def get_rxn_containing(self, formulas):
        """
        Find reactions that contain all formulas given.
        Args:
            formulas: list of formulas. string okay if one formula.
        Returns:
            reaction details
        """
        if isinstance(formulas, str):
            formulas = list(formulas)
        return sorted(
            [
                (
                    self.reactions[i]["barrier"],
                    self.reactions[i]["summary"],
                    self.reactions[i]["n_competing"],
                    i,
                )
                for i in self.reactions
                if all(
                    [formula in self.reactions[i]["summary"] for formula in formulas]
                )
            ]
        )

    def check_if_known_precursors(self):
        with open(
            os.path.join(settings.rxn_files, "experimental_precursors_KononovaSciData.json"), "r"
        ) as f:
            exp_precursors = set(json.load(f))
        exp_precursors = exp_precursors.union(set(self.explicit_includes))

        for i in self.reactions:
            ids = [
                self.reactions[i]["precursor_ids"][j]
                for j in range(len(self.reactions[i]["precursor_ids"]))
                if self.reactions[i]["precursor_formulas"][j] not in GASES
            ]
            frac = len(set(ids).intersection(exp_precursors)) / len(ids)
            self.reactions[i]["exp_precursors"] = str(np.round(frac, decimals=4))

    def get_pareto_front(self):
        """
        Returns: list of reaction labels on the pareto front
        """
        x = self.plot_data[self.plot_data["barrier"] < np.inf].sort_values(
            by=["n_competing", "barrier"]
        )[["n_competing", "barrier"]]
        y = x.groupby(by=["n_competing"], as_index=False).min()
        rows = list(y.iterrows())
        front = []
        barrier_front = []
        for row in rows:
            n_competing = row[1]["n_competing"]
            barrier = row[1]["barrier"]
            if rows.index(row) == 0:
                front.append(
                    x.index[
                        (x["barrier"] == barrier) & (x["n_competing"] == n_competing)
                    ][0]
                )
                barrier_front.append(barrier)
                continue
            if barrier < barrier_front[-1]:
                front.append(
                    x.index[
                        (x["barrier"] == barrier) & (x["n_competing"] == n_competing)
                    ][0]
                )
                barrier_front.append(barrier)
        return front

    def topsis(self, latex=False):
        """
        Returns a ranked list of reactions based on TOPSIS method for multiobjective optimization.
        Returns:
        """
        x = self.plot_data[["n_competing", "barrier"]]
        x = x[x["barrier"] < np.inf]
        xsum = np.sqrt((x ** 2).sum())
        mu = x / xsum
        positive_ideal = mu.min()
        negative_ideal = mu.max()
        d_pos_ideal = np.sqrt(((mu - positive_ideal) ** 2).sum(axis=1))
        d_neg_ideal = np.sqrt(((mu - negative_ideal) ** 2).sum(axis=1))
        x["topsis_score"] = d_neg_ideal / (d_pos_ideal + d_neg_ideal)
        x = x.sort_values(by="topsis_score", ascending=False)
        result = self.plot_data.loc[x.index]
        result["topsis_score"] = x["topsis_score"]

        if latex:
            result["summary"] = result["summary"].apply(latexify)
        return result

    @staticmethod
    def get_material_id_from_formula(formula_str: str) -> str:
        with get_mprester() as mpr:
            options = mpr.query(
                {"pretty_formula": Composition(formula_str).reduced_formula},
                ["material_id", "e_above_hull"]
            )
            if not options:
                raise ValueError("{} query failed, please enter valid formula or mp id".format(formula_str))
            options = sorted(options, key=lambda x: x["e_above_hull"])
            return options[0]["material_id"]

from typing import List, Union, Optional

from plotly.graph_objs import Figure
from pydantic import BaseModel, Field, NonNegativeInt, create_model


class RecommendRoutesRequest(BaseModel):
    target_entry_id: str = Field(
        ...,
        description="enter mp-id or formula"
    )
    confine_to_icsd: bool = Field(
        True,
        description="Use ICSD-sourced entries to find precursors."
    )
    confine_to_stables: bool = Field(
        True,
        description="Use stable entries only to find."
    )
    hull_distance: Optional[float] = Field(
        None,
        description="Use entries within this distance to hull (eV/atom). Can significantly increase \
                number of possible precursors and slow down the predictions. Ignored if confine_to_stables is True."
    )
    simple_precursors: NonNegativeInt = Field(
        0,
        description="If > 0, precursors with fewer components will be considered."
    )
    explicit_includes: List[str] = Field(
        [],
        description="list of mp-ids to explicitly include. For example, confine_to_stables may exclude \
                certain common precursors in some systems, if they are not on the convex-hull - this allows such \
                potential precursors to be added to the library."
    )
    add_elements: List[str] = Field(
        [],
        description=(
            "Add elements to the chemical space of libraries that doesn't exist in the target"
            " material. Best example is 'C', which would allow carbonates to be added to the precursor library."
        )
    )
    exclude_compositions: List[str] = Field(
        [],
        description="list of compositions to avoid in precursor library."
    )
    sigma: float = Field(
        2 * 6.242 * 0.01,
        description="surface energy constant (eV/Ang^2) to be used in predictions. Defaults to equivalent \
                2.0 J/m^2."
    )
    transport_constant: float = Field(
        10,
        description="diffusion barrier coefficient (max barrier)"
    )
    flexible_competition: NonNegativeInt = Field(
        0,
        description="whether lower order targets are allowed in competing reactions. Defaults to 0 \
                which forces competing reactions to have products of the same order as target. If 1, one order smaller \
                compounds and so on."
    )

    temperature: float = Field(
        1600,
        description="Temperature (in Kelvin) to consider in free energy adjustments for gases."
    )
    pressure: Union[float, dict] = Field(
        0.001,
        description=(
            "Gas pressures (in atm). If float, all gases are assumed to have the same constant"
            " pressure. A dictionary in the form of {'O2': 0.21, 'CO2':, 0.05} can be provided to explicitly"
            " specify partial pressures. If given None, a default pressure dictionary will be used pertaining to"
            " open atmosphere conditions."
        )
    )
    allow_gas_release: bool = Field(
        False,
        description="Allow for gaseous reaction products, e.g. O2, CO2"
    )
    max_component_precursors: int = 0
    show_fraction_known_precursors: bool = Field(
        False,
        description="Show the fraction of known synthetic reagents in reaction"
    )
    show_known_precursors_only: bool = Field(
        False,
        description="Show only reactions with known precursors"
    )
    confine_competing_to_icsd: bool = Field(
        False,
        description="Confine competing reactions to those containing ICSD materials"
    )
    display_peroxides: bool = Field(
        False,
        description="Show reactions involving peroxide compounds"
    )
    display_superoxides: bool = Field(
        False,
        description="Show reactions involving superoxide compounds"
    )
    add_pareto: bool = Field(
        False,
        description="Show the Pareto front on the reaction analysis diagram"
    )


PlotlyFigureResponse = create_model('PlotlyFigureResponse', **Figure().to_dict())

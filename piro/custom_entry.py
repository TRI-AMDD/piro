import re
from typing import Optional

from pymatgen.core import Composition, Structure
from pymatgen.entries.compatibility import MaterialsProjectCompatibility
from pymatgen.entries.computed_entries import ComputedEntry, ComputedStructureEntry
from pymatgen.io.vasp.sets import MPRelaxSet

# copied from https://github.com/TRI-AMDD/CAMD/blob/a466e8493a84e4fdb236a07acc32b6f217e5d49a/camd/experiment/dft.py#L870
MP_REFERENCES = {
    "H": -3.39271585,
    "He": -0.00902216,
    "Li": -1.9089228533333333,
    "Be": -3.739412865,
    "B": -6.679390641666667,
    "C": -9.22676982,
    "N": -8.336493965,
    "O": -4.94795546875,
    "F": -1.9114557725,
    "Ne": -0.02582742,
    "Na": -1.312223005,
    "Mg": -1.5968959166666667,
    "Al": -3.74557583,
    "Si": -5.423390655,
    "P": -5.413285861428571,
    "S": -4.136449866875,
    "Cl": -1.8485262325,
    "Ar": -0.06880822,
    "K": -1.110398947,
    "Ca": -1.999462735,
    "Sc": -6.332469105,
    "Ti": -7.895052840000001,
    "V": -9.08235617,
    "Cr": -9.65304747,
    "Mn": -9.161706470344827,
    "Fe": -8.46929704,
    "Co": -7.108317795,
    "Ni": -5.7798218,
    "Cu": -4.09920667,
    "Zn": -1.259460605,
    "Ga": -3.02808992,
    "Ge": -4.61751163,
    "As": -4.65850806,
    "Se": -3.49591147765625,
    "Br": -1.63692654,
    "Kr": -0.05671467,
    "Rb": -0.9805340725,
    "Sr": -1.6894812533333334,
    "Y": -6.466074656666667,
    "Zr": -8.54770063,
    "Nb": -10.10130504,
    "Mo": -10.84563514,
    "Tc": -10.36061991,
    "Ru": -9.27438911,
    "Rh": -7.33850956,
    "Pd": -5.17648694,
    "Ag": -2.8325290566666665,
    "Cd": -0.90620278,
    "In": -2.75168373,
    "Sn": -3.99229498,
    "Sb": -4.128999585,
    "Te": -3.14330093,
    "I": -1.524009065,
    "Xe": -0.03617417,
    "Cs": -0.8954023720689656,
    "Ba": -1.91897083,
    "La": -4.936007105,
    "Ce": -5.933089155,
    "Pr": -4.780899145,
    "Nd": -4.76814321,
    "Pm": -4.7505423225,
    "Sm": -4.717682476666667,
    "Eu": -10.292043475,
    "Gd": -14.07612224,
    "Tb": -4.6343661,
    "Dy": -4.60678684,
    "Ho": -4.58240887,
    "Er": -4.5674248,
    "Tm": -4.475058396666666,
    "Yb": -1.5395952733333333,
    "Lu": -4.52095052,
    "Hf": -9.95718477,
    "Ta": -11.85777728,
    "W": -12.95812647,
    "Re": -12.444527185,
    "Os": -11.22733445,
    "Ir": -8.83843042,
    "Pt": -6.07090771,
    "Au": -3.27388154,
    "Hg": -0.30362902,
    "Tl": -2.36165292,
    "Pb": -3.71258955,
    "Bi": -3.88641638,
    "Ac": -4.1211750075,
    "Th": -7.41385825,
    "Pa": -9.51466466,
    "U": -11.29141001,
    "Np": -12.94777968125,
    "Pu": -14.26782579,
}


def get_mp_formation_energy(total_e, formula, potcar_symbols, hubbards={}, explain=False):
    """
    Helper function to computer mp-compatible formation
    energy using reference energies extracted from MP
    Args:
        total_e (float): total energy (uncorrected)
        formula (str): chemical formula
        potcar_symbols (list): list of potcar symbols
        hubbards (dict): hubbard value, if none, the
                        run_type = 'GGA'
                        else run_type = 'GGA+U'
        explain (bool): whether to print out the explanation
                        of the correction
    Returns:
        (float): mp-compatible formation energy (eV/atom)
    """
    compatibility = MaterialsProjectCompatibility()
    comp = Composition(formula)
    run_type = "GGA+U" if hubbards else "GGA"
    is_hubbard = True if hubbards else False
    entry = ComputedEntry(
        composition=comp,
        energy=total_e,
        parameters={
            "potcar_symbols": potcar_symbols,
            "run_type": run_type,
            "hubbards": hubbards,
            "is_hubbard": is_hubbard,
        },
    )
    # process_entry has a bad try/except block that makes it difficult to catch errors,
    # use this instead
    entry = compatibility.process_entries([entry])[0]
    if explain:
        print(compatibility.explain(entry))
    energy = entry.energy
    for el, occ in comp.items():
        energy -= MP_REFERENCES[el.name] * occ
    return energy / comp.num_atoms


def get_mp_formation_energy_from_m3gnet(total_e, structure, explain=False):
    """
    Hack to get materials-project compatible formation energy from m3gnet
    by overriding potcar/hubbard values with default values from MPRelaxSet
    """
    vaspset = MPRelaxSet(structure)
    potcar_symbols = ["PBE {}".format(sym) for sym in vaspset.potcar_symbols]
    symbols = [s.split()[1] for s in potcar_symbols]
    symbols = [re.split(r"_", s)[0] for s in symbols]
    if not vaspset.incar.get("LDAU", False):
        hubbards = {}
    else:
        us = vaspset.incar.get("LDAUU")
        js = vaspset.incar.get("LDAUJ")
        if len(js) != len(us):
            js = [0] * len(us)
        if len(us) == len(symbols):
            hubbards = {symbols[i]: us[i] - js[i] for i in range(len(symbols))}
        elif sum(us) == 0 and sum(js) == 0:
            hubbards = {}
    return get_mp_formation_energy(
        total_e, structure.composition.formula, potcar_symbols=potcar_symbols, hubbards=hubbards, explain=explain
    )


def create_custom_entry(
    cif_string: str, formation_energy_per_atom: Optional[float] = None, entry_id: Optional[str] = None
) -> ComputedStructureEntry:
    """
    with comments from joseph.montoya@tri.global

    :param cif_string: from a .cif file from pymatgen representing a Structure
    :param formation_energy_per_atom: if not provided, use m3gnet
    :param entry_id: provide a custom entry name
    :return:
    """
    structure = Structure.from_str(cif_string, "cif")
    structure.entry_id = entry_id or "custom_entry"

    if formation_energy_per_atom is None:
        try:
            from m3gnet.models import Relaxer
        except ImportError:
            raise ImportError(
                "m3gnet is required to calculate formation energy for custom entry, when no formation "
                'energy is provided. Run "pip install piro[m3gnet]".'
            )
        relaxer = Relaxer()
        trajectory = relaxer.relax(structure)["trajectory"]
        energy = trajectory.energies[-1].flatten()[0]
        formation_energy_per_atom = get_mp_formation_energy_from_m3gnet(energy, structure)

    """
    it shouldn't matter in the case of user-specified, 
    since we're computing competing reactions on the basis of formation energies, 
    rather than using the phase diagram explicitly
    """
    dummy_energy = 123456789

    custom_entry = ComputedStructureEntry(structure, dummy_energy, entry_id=structure.entry_id)
    custom_entry.data["formation_energy_per_atom"] = formation_energy_per_atom

    """
    the structure.perturb isn't strictly necessary 
    but sometimes is useful to fix issues in voronoi featurization that happens when computing the similarity metrics
    """
    custom_entry.structure.perturb(0.01)

    """
    it is possible that the user-supplied structure could match an ICSD structure, 
    I don't think we should worry about that, i.e. it's safe to just make it an empty list I think
    """
    custom_entry.data["icsd_ids"] = []

    return custom_entry

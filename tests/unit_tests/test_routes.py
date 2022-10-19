import os
import unittest
import warnings
from pathlib import Path
from pymatgen.ext.matproj import MPRester, MPRestError, _MPResterLegacy
from pymatgen.core import SETTINGS
from _pytest.monkeypatch import MonkeyPatch
from monty.serialization import loadfn, dumpfn
from piro.route import SynthesisRoutes

TEST_FILES = Path(__file__).absolute().parent / "test_files"


class RoutesTest(unittest.TestCase):
    def setUp(self):
        # Monkeypatch if MAPI key not detected
        self.monkeypatch = MonkeyPatch()

        try:
            MPRester().get_entry_by_material_id('mp-5020')
        except (MPRestError, ValueError):
            warnings.warn("Using mock MPRester response")

            def get_entries_in_chemsys(*args, **kwargs):
                return loadfn(TEST_FILES / "ba-o-ti.json")

            def get_entry_by_material_id(*args, **kwargs):
                return loadfn(TEST_FILES / "ba-o-ti.json")[74]

            def get_database_version(*args, **kwargs):
                return None

            self.monkeypatch.setattr(
                _MPResterLegacy, "get_entries_in_chemsys", get_entries_in_chemsys)
            self.monkeypatch.setattr(
                _MPResterLegacy, "get_entry_by_material_id", get_entry_by_material_id)
            self.monkeypatch.setattr(
                _MPResterLegacy, "get_database_version", get_database_version)

    def test_basic_route(self):
        # BaTiO3 example
        route = SynthesisRoutes(
            "mp-5020",
            epitaxies={k.replace('mp-5020', '').strip('_'): v for k, v in loadfn(TEST_FILES / "_epitaxy_cache.json").items()},
            similarities={k.replace('mp-5020', '').strip('_'): v for k, v in loadfn(TEST_FILES / "_epitaxy_cache.json").items()}
        )
        route.recommend_routes(temperature=298)

    def tearDown(self) -> None:
        self.monkeypatch.undo()


def dump_tdata():
    """Quick helper function to dump data for future reference"""
    with MPRester() as mpr:
        data = mpr.get_entries_in_chemsys(
            ["Ba", "Ti", "O"], inc_structure="final",
            property_data=["icsd_ids", "formation_energy_per_atom"])
    dumpfn(data, TEST_FILES / "ba-o-ti.json")
    return data


if __name__ == '__main__':
    unittest.main()

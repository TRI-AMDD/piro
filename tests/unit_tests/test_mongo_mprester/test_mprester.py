import json
from pathlib import Path
from unittest.mock import patch

import pytest
from pymatgen.core import Composition
from pymatgen.entries.computed_entries import ComputedEntry, ComputedStructureEntry
from piro.mprester import get_mprester, MongoMPRester


@pytest.fixture(scope='class')
def mongo_mprester():
    with get_mprester() as mpr:
        if not isinstance(mpr, MongoMPRester):
            pytest.skip("only test this using real mongo db")
        yield mpr


class TestMongoMPResterWithRealDB:
    """
    makes sure mongo db has the information we need to replicate MP API
    """

    def test_get_entry_by_material_id(self, mongo_mprester):
        reference_file = Path(__file__).absolute().parent / "mp-9029_entry_by_material_id.json"

        e = mongo_mprester.get_entry_by_material_id('mp-9029')

        assert e == ComputedEntry.from_dict(json.load(open(reference_file)))

    def test_get_entries_in_chemsys(self, mongo_mprester):
        reference_file = Path(__file__).absolute().parent / "mp-9029_entries_in_chemsys.json"

        entries = mongo_mprester.get_entries_in_chemsys(
            ['Ca', 'V', 'N'],
            inc_structure="final",
            property_data=["icsd_ids", "formation_energy_per_atom"]
        )

        ref_entries = [ComputedStructureEntry.from_dict(json.loads(e)) for e in json.load(open(reference_file))]
        assert sorted(entries, key=lambda x: x.entry_id) == sorted(ref_entries, key=lambda x: x.entry_id)

    def test_get_material_id_from_formula(self, mongo_mprester):
        result = mongo_mprester.query(
            {"pretty_formula": Composition("Ca3VN3").reduced_formula},
            ["material_id", "e_above_hull"]
        )

        assert result == [{'material_id': 'mp-9029', 'e_above_hull': 0}]


@patch(f'{get_mprester.__module__}.MongoClient')
class TestMongoMPResterMocked:

    def test_query(self, mongo_client_mock):
        mock_result = [{'material_id': 'mp-9029', 'e_above_hull': 0}]
        mock_uri = 'some_uri'
        mongo_client_mock.return_value.piro.mp.find.return_value = mock_result

        with MongoMPRester(mock_uri) as mpr:
            res = mpr.query({}, [])

        mongo_client_mock.assert_called_once_with(mock_uri)
        mongo_client_mock.return_value.close.assert_called_once_with()
        mongo_client_mock.return_value.piro.mp.find.assert_called_once_with({}, {'_id': False})
        assert res == mock_result

    def test_query_with_task_id(self, mongo_client_mock):
        mock_uri = 'some_uri'
        mongo_client_mock.return_value.piro.mp.find.return_value = [{'material_id': 'mp-9029', 'e_above_hull': 0}]

        with MongoMPRester(mock_uri) as mpr:
            res = mpr.query({'task_id': 'mp-9029'}, ['task_id'])

        mongo_client_mock.assert_called_once_with(mock_uri)
        mongo_client_mock.return_value.close.assert_called_once_with()
        mongo_client_mock.return_value.piro.mp.find.assert_called_once_with(
            {'material_id': 'mp-9029'},
            {'_id': False, 'material_id': True}
        )
        assert res == [{'material_id': 'mp-9029', 'e_above_hull': 0, 'task_id': 'mp-9029'}]

import pytest

from piro.custom_entry import create_custom_entry

custom_entry_cif_string = """# generated using pymatgen
data_Li4RuO5
_symmetry_space_group_name_H-M   Cmcm
_cell_length_a   4.07830800
_cell_length_b   9.64177000
_cell_length_c   9.72921500
_cell_angle_alpha   90.00000000
_cell_angle_beta   90.00000000
_cell_angle_gamma   90.00000000
_symmetry_Int_Tables_number   63
_chemical_formula_structural   Li4RuO5
_chemical_formula_sum   'Li16 Ru4 O20'
_cell_volume   382.57324031
_cell_formula_units_Z   4
loop_
 _symmetry_equiv_pos_site_id
 _symmetry_equiv_pos_as_xyz
  1  'x, y, z'
  2  '-x, -y, -z'
  3  '-x, -y, z+1/2'
  4  'x, y, -z+1/2'
  5  'x, -y, -z'
  6  '-x, y, z'
  7  '-x, y, -z+1/2'
  8  'x, -y, z+1/2'
  9  'x+1/2, y+1/2, z'
  10  '-x+1/2, -y+1/2, -z'
  11  '-x+1/2, -y+1/2, z+1/2'
  12  'x+1/2, y+1/2, -z+1/2'
  13  'x+1/2, -y+1/2, -z'
  14  '-x+1/2, y+1/2, z'
  15  '-x+1/2, y+1/2, -z+1/2'
  16  'x+1/2, -y+1/2, z+1/2'
loop_
 _atom_site_type_symbol
 _atom_site_label
 _atom_site_symmetry_multiplicity
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
  Li  Li0  8  0.00000000  0.09507969  0.09696528  1
  Li  Li1  8  0.00000000  0.40193404  0.09618901  1
  Ru  Ru2  4  0.00000000  0.25132373  0.75000000  1
  O  O3  8  0.00000000  0.11207412  0.61064667  1
  O  O4  8  0.00000000  0.39083833  0.61108810  1
  O  O5  4  0.00000000  0.24870859  0.25000000  1
"""


@pytest.mark.parametrize("formation_energy,entry_id", [(None, None), (1.2, "my_id")])
def test_create_custom_entry_default(formation_energy, entry_id):
    # when
    custom_entry = create_custom_entry(custom_entry_cif_string, formation_energy, entry_id)

    # then
    assert custom_entry.entry_id == (entry_id or "custom_entry")
    assert round(custom_entry.data["formation_energy_per_atom"], 1) == (formation_energy or -1.9)

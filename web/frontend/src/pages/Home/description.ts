export const description = {
  target_entry_id: 'Materials Project ID of the compound to synthesize',
  max_component_precursors:
    'Used to limit the reactants to simpler sub-chemistries<br> of our target to obtain a refined precursor list. <br> For example, setting this as 2 for a ternary target compound <br> would limit precursors to binary compounds<br> (additional element count ignored)',
  flexible_competition:
    'Used to limit the reactants to simpler sub-chemistries<br> of our target to obtain a refined precursor list. <br> For example,setting this as 2 for a ternary target compound would limit precursors <br> to binary compounds<br> (additional element count ignored)',
  hull_distance: 'Deselect “Stable precursors only” checkbox<br> if you wish to edit “Distance of Hull”.<br>This defines the energy range of metastable materials<br> for inclusion for inclusion in precursor library.',
  add_elements: 'For example, to include carbonates and carbides, select C here.',
  explicit_includes: 'List of Materials Project IDs of additional materials to include in precursor list',
  allow_gas_release: 'Reactions are balanced such that O2, CO2 etc. can be released alongside the target',
  confine_to_stables: 'Deselect “Stable precursors only” checkbox<br> if you wish to edit “Distance of Hull”.<br>This confines the precursor library<br> to thermodynamically stable materials in MP',
  confine_to_icsd:
    'Confines the precursur library to materials in MP <br> sourced from the Inorganic Crystal Structures Database',
  simple_precursors:
    'Lower order compounds are considered <br> if greater than zero <br> (e.g., 1 means a ternary target would<br> consider up to binaries in precursors)',
  exclude_compositions: 'Materials that have these exact formulas<br> are excluded from the precursor library',
  confine_competing_to_icsd: 'Confine competing<br> reactions<br> to those containing<br> ICSD materials',
  pressure:
    'Sets pressure of gas phases. Can specify a constant pressure,<br> the ambient partial pressures or a custom dictionary.'
};

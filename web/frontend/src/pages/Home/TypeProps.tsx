export interface Inputs {
  target_entry_id: string | null;
  custom_entry_cif_string: string | null;
  custom_entry_formation_energy_per_atom: number;
  confine_to_icsd: boolean;
  confine_to_stables: boolean;
  hull_distance: number;
  simple_precursors: number;
  example: string;
  explicit_includes: string[];
  add_elements: string[];
  exclude_compositions: string[];
  sigma: number;
  transport_constant: number;
  flexible_competition: number;
  temperature: number;
  pressure: number;
  max_component_precursors: number;
  allow_gas_release: boolean;
  show_fraction_known_precursors: boolean;
  show_known_precursors_only: boolean;
  confine_competing_to_icsd: boolean;
  display_peroxides: boolean;
  display_superoxides: boolean;
  add_pareto: boolean;
}

export type Option = { label: string; value: string };

export interface Inputs {
    target_entry_id: string;
    confine_to_icsd: boolean;
    confine_to_stables: boolean;
    example: string;
    add_elements: string[];
    temperature: number;
    pressure: number;
    max_component_precursors: number;
    allow_gas_release: boolean;
    show_fraction_known_precursors: boolean;
    show_known_precursors_only: boolean;
    confine_competing_to_icsd: boolean;
    display_peroxides: boolean;
    add_pareto: boolean;
}

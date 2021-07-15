export interface Inputs {
    formula: string;
    example: string;
    add_elements: string;
    temperature: number;
    pressure: number;
    max_component_precursors: number;
    synthesis_bool_options: {
        allowGasRelease: boolean;
        showFractionKnownPrecursors: boolean;
        showKnownPrecursorsOnly: boolean;
        confineCompetingToIcsd: boolean;
        displayPeroxides: boolean;
        addPareto: boolean;
    }
}

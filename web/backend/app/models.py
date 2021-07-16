from typing import List, Union

from pydantic import BaseModel, Field


class SynthesisBoolOptions(BaseModel):
    allow_gas_release: bool = Field(
        False,
        description="Allow for gaseous reaction products, e.g. O2, CO2"
    )
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
    add_pareto: bool = Field(
        False,
        description="Show the Pareto front on the reaction analysis diagram"
    )


class RecommendRoutesForm(BaseModel):
    mp_id: str = Field(
        ...,
        description="enter mp-id or formula"
    )
    temperature: float = Field(
        298,
        description="Temperature (in Kelvin) to consider in free energy adjustments for gases."
    )
    pressure: Union[float, dict] = Field(
        1,
        description=(
            "Gas pressures (in atm). If float, all gases are assumed to have the same constant"
            " pressure. A dictionary in the form of {'O2': 0.21, 'CO2':, 0.05} can be provided to explicitly"
            " specify partial pressures. If given None, a default pressure dictionary will be used pertaining to"
            " open atmosphere conditions."
        )
    )
    max_component_precursors: int = 0
    add_elements: List[str] = Field(
        [],
        description=(
            "Add elements to the chemical space of libraries that doesn't exist in the target"
            " material. Best example is 'C', which would allow carbonates to be added to the precursor library."
        )
    )
    synthesis_bool_options: SynthesisBoolOptions = SynthesisBoolOptions()



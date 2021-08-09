from enum import Enum
from typing import List, Union, Optional

from plotly.graph_objs import Figure
from pydantic import BaseModel, Field, NonNegativeInt, create_model


class RecommendRoutesRequest(BaseModel):
    target_entry_id: str = Field(
        ...,
        description="Materials Project ID of the compound to synthesize"
    )
    confine_to_icsd: bool = Field(
        True,
        description="Confines the precursur library to materials in MP sourced \
        from the Inorganic Crystal Structures Database"
    )
    confine_to_stables: bool = Field(
        True,
        description="Confines the precursur library to thermodynamically stable materials in MP"
    )
    hull_distance: Optional[float] = Field(
        None,
        description="Distance to Hull (eV/atom). \
        Defines the energy range of metastable materials for inclusion in precursor library."
    )
    simple_precursors: NonNegativeInt = Field(
        0,
        description="Lower order compounds are considered if greater than zero \
        (e.g. 1 means a ternary target would consider up to binaries in precusors)"
    )
    explicit_includes: List[str] = Field(
        [],
        description="List of Materials Project IDs of additional materials to include in precursor list"
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
        description="Materials that have these exact formulas are excluded from the precursor library"
    )
    sigma: float = Field(
        2 * 6.242 * 0.01,
        description="surface energy scaling factory (eV/Ang^2) to be used in predictions. Defaults to equivalent \
                2.0 J/m^2."
    )
    transport_constant: float = Field(
        10,
        description="Transport barrier. Diffusion barrier coefficient (max barrier)"
    )
    flexible_competition: NonNegativeInt = Field(
        0,
        description="This parameter can add resolution to the phase competition axis. \
        For example, 0 includes only the competing phases that have the same number of elements as the target, \
        whereas 1 would include phases that may also have one less element and so on. \
        A good heuristic is 1 if more resolution is needed on x-axis."
    )

    temperature: float = Field(
        1000,
        description="Temperature (in Kelvin) to consider in free energy adjustments for gases."
    )
    pressure: Optional[Union[float, dict]] = Field(
        1,
        description=(
            "Sets pressure (atm) of gas phases. Can specify a constant pressure, a custom dictionary, \
            or None which will use the ambient partial pressures (see piro.data.DEFAULT_GAS_PRESSURES)"
        )
    )
    allow_gas_release: bool = Field(
        False,
        description="Allow for gaseous reaction products. \
        Reactions are balanced such that O2, CO2 etc. can be released alongside the target"
    )
    max_component_precursors: int = Field(
        0,
        description="Maximum number of components in precursors. Used to limit the reactants \
        to simpler sub-chemistries of our target to obtain a refined precursor list. \
        For example, setting this as 2 for a ternary target compound would limit precursors to \
        binary compounds (additional element count ignored)"
    )
    show_fraction_known_precursors: bool = Field(
        False,
        description="Show the fraction of known precursors in reaction"
    )
    show_known_precursors_only: bool = Field(
        False,
        description="Show only reactions with known precursors"
    )
    confine_competing_to_icsd: bool = Field(
        False,
        description="ICSD-based Parasitic Phases Only. Confine competing reactions to those containing ICSD materials"
    )
    display_peroxides: bool = Field(
        False,
        description="Show reactions involving peroxides"
    )
    display_superoxides: bool = Field(
        False,
        description="Show reactions involving superperoxides"
    )
    add_pareto: bool = Field(
        False,
        description="Show the Pareto front on the reaction analysis diagram"
    )


PlotlyFigureResponse = create_model('PlotlyFigureResponse', **Figure().to_dict())


class RecommendRoutesTaskStatus(str, Enum):
    PENDING = 'pending'
    INVALID = 'invalid'
    STARTED = 'started'
    FAILURE = 'failure'
    SUCCESS = 'success'


class RecommendRoutesTask(BaseModel):
    task_id: Optional[str] = None
    request: Optional[RecommendRoutesRequest] = None
    status: RecommendRoutesTaskStatus = RecommendRoutesTaskStatus.INVALID
    error_message: Optional[str] = None
    result: Optional[PlotlyFigureResponse] = None

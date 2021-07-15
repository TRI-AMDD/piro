from typing import Optional, List

from pydantic import BaseModel


class SynthesisBoolOptions(BaseModel):
    allow_gas_release: bool = False
    show_fraction_known_precursors: bool = False
    show_known_precursors_only: bool = False
    confine_competing_to_icsd: bool = False
    display_peroxides: bool = False
    add_pareto: bool = False


class RecommendRoutesForm(BaseModel):
    mp_id: str
    temperature: float = 1600.0
    pressure: Optional[int] = None
    max_component_precursors: int = 2
    add_elements: List[str] = []
    synthesis_bool_options: SynthesisBoolOptions = SynthesisBoolOptions()



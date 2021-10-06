import json
from pathlib import Path

from app.models import RecommendRoutesRequest

requests = dict(
    Ca3VN3=RecommendRoutesRequest(
        target_entry_id='mp-9029',
        temperature=1600,
        pressure=0.001,
        max_component_precursors=2,
        show_fraction_known_precursors=False,
        show_known_precursors_only=False,
        display_peroxides=True,
        add_pareto=True
    ).dict(exclude_unset=True),
    BaTiO3=RecommendRoutesRequest(
        target_entry_id='mp-5986',
        confine_to_icsd=True,
        confine_to_stables=True,
        explicit_includes=['mp-3943', 'mp-1203', 'mp-2657', 'mp-4559'],
        exclude_compositions=['BaTiO3'],
        allow_gas_release=True,
        confine_competing_to_icsd=False,
        add_elements=['C'],
        temperature=1400,
        max_component_precursors=2,
        show_fraction_known_precursors=False,
        show_known_precursors_only=False,
        display_peroxides=True,
        add_pareto=True
    ).dict(exclude_unset=True),
    RuSr2GdCu2O8=RecommendRoutesRequest(
        target_entry_id='mp-1104173',
        confine_to_icsd=True,
        confine_to_stables=True,
        explicit_includes=['mp-1079192'],
        exclude_compositions=['SrCu', 'SrCu5', 'GdCu', 'GdCu2', 'GdCu5', 'GdRu2', 'RuO4'],
        add_elements=["C"],
        flexible_competition=1,
        confine_competing_to_icsd=False,
        allow_gas_release=True,
        temperature=900,
        pressure=10.0,
        max_component_precursors=4,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False,
        add_pareto=True,
    ).dict(exclude_unset=True),
    Ba2Ti9O20=RecommendRoutesRequest(
        target_entry_id='mp-560731',
        confine_to_icsd=True,
        explicit_includes=['mp-2657', 'mp-27790', 'mp-3175', 'mp-5986'],
        confine_to_stables=True,
        allow_gas_release=True,
        confine_competing_to_icsd=False,
        temperature=1300,
        max_component_precursors=3,
        show_known_precursors_only=True,
        display_peroxides=False,
        display_superoxides=False
    ).dict(exclude_unset=True),
    Ba2YTaO6=RecommendRoutesRequest(
        target_entry_id='mp-6613',
        confine_to_icsd=True, add_elements=['C'],
        confine_to_stables=True, explicit_includes=['mp-10390'],
        exclude_compositions=['Y4C5', 'Y3C4', 'Y2C', 'Y4C7', 'TaC', 'Ta2C'],
        flexible_competition=1,
        allow_gas_release=True,
        confine_competing_to_icsd=False,
        temperature=1600,
        pressure=None,
        max_component_precursors=3,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False, add_pareto=True,
    ).dict(exclude_unset=True),
    BaV10O15=RecommendRoutesRequest(
        target_entry_id='mp-19458',
        confine_to_icsd=True, add_elements=['C'],
        confine_to_stables=True,
        allow_gas_release=True,
        confine_competing_to_icsd=False,
        explicit_includes=['mp-19184', 'mp-19365', 'mp-18937'],  # 'mp-1273331'],
        flexible_competition=1, temperature=1800,
        max_component_precursors=3,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False, add_pareto=True,
        pressure=0.1,
    ).dict(exclude_unset=True),
    Ca2CrSbO6=RecommendRoutesRequest(
        target_entry_id='mp-1189906',
        temperature=1400, pressure=None, show_fraction_known_precursors=False,
        max_component_precursors=2, display_peroxides=True, add_pareto=True
    ).dict(exclude_unset=True),
    CaSnSiO5=RecommendRoutesRequest(
        target_entry_id='mp-6809',
        confine_to_icsd=True,
        allow_gas_release=True,
        confine_competing_to_icsd=False,
        confine_to_stables=True, explicit_includes=['mp-4438', 'mp-7000', 'mp-6945'],
        flexible_competition=0, temperature=1600,
        max_component_precursors=3,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False, add_pareto=True,
    ).dict(exclude_unset=True),
    K2Mo9S11=RecommendRoutesRequest(
        target_entry_id='mp-29784',
        confine_to_icsd=True,  # explicit_includes=['mp-1434'],
        confine_to_stables=False,
        hull_distance=0.0,
        flexible_competition=1,
        allow_gas_release=True,
        confine_competing_to_icsd=False,
        temperature=1500,
        pressure=0.00000001,
        max_component_precursors=3,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False, add_pareto=True,
    ).dict(exclude_unset=True),
    K2V3P4O17=RecommendRoutesRequest(
        target_entry_id='mp-29784',
        explicit_includes=["mp-557105", "mp-21579", "mp-19094"],
        allow_gas_release=False,
        confine_competing_to_icsd=False,
        temperature=900,
        pressure=None,
        max_component_precursors=3,
        show_fraction_known_precursors=False,
        show_known_precursors_only=True,
        display_peroxides=False,
        display_superoxides=False,
        add_pareto=True
    ).dict(exclude_unset=True),
    K3Y_VO4_2=RecommendRoutesRequest(
        target_entry_id='mp-1105034',
        confine_to_icsd=True,  # add_element='C',
        confine_to_stables=True,  # explicit_includes=['mp-1180742'],
        flexible_competition=1,
        temperature=1300,
        pressure=None,
        allow_gas_release=True,
        max_component_precursors=3,
        confine_competing_to_icsd=False,
        show_known_precursors_only=True,
        show_fraction_known_precursors=False,
        display_peroxides=True,
        display_superoxides=True, add_pareto=True,
    ).dict(exclude_unset=True),
    LiNa5Mo9O30=RecommendRoutesRequest(
        target_entry_id='mp-1195001',
        add_elements=['C'], explicit_includes=['mp-18050'], pressure=None,
        temperature=1100, allow_gas_release=True,
        show_known_precursors_only=False, confine_competing_to_icsd=False,
        max_component_precursors=3,
        show_fraction_known_precursors=False,
        display_peroxides=True,
        add_pareto=True,
    ).dict(exclude_unset=True),
    RbFe_MoO4_2=RecommendRoutesRequest(
        target_entry_id='mp-18868',
        confine_to_icsd=True,
        confine_to_stables=True,
        explicit_includes=['mp-1193851', 'mp-704851', 'mp-1394'],
        flexible_competition=1,
        temperature=900,
        pressure=None,
        allow_gas_release=True,
        max_component_precursors=3,
        confine_competing_to_icsd=False,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False, add_pareto=True,
    ).dict(exclude_unset=True),
    Sr2CoMoO6=RecommendRoutesRequest(
        target_entry_id='mp-510546',
        confine_to_icsd=True, add_elements=['C'],
        confine_to_stables=True, explicit_includes=['mp-17289', 'mp-18748'],  # CoMoO4, Co3O4
        flexible_competition=1,
        temperature=1400,
        pressure=None,
        allow_gas_release=True,
        max_component_precursors=3,
        confine_competing_to_icsd=False,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=True,
        display_superoxides=False, add_pareto=True
    ).dict(exclude_unset=True),
    Sr2FeO3F=RecommendRoutesRequest(
        target_entry_id='mp-19293',
        add_elements=['C'], explicit_includes=["mp-19770"],
        temperature=1500,
        pressure=None,
        allow_gas_release=True,
        max_component_precursors=2,
        show_fraction_known_precursors=False,
        show_known_precursors_only=False,
        confine_competing_to_icsd=False,
        display_peroxides=False,
        add_pareto=True
    ).dict(exclude_unset=True),
    Sr2NiWO6=RecommendRoutesRequest(
        target_entry_id='mp-20794',
        confine_to_icsd=True,
        add_elements=['C'],
        confine_to_stables=True,  # explicit_includes=['mp-10390'],
        flexible_competition=1,
        temperature=1700,
        pressure=None,
        allow_gas_release=True,
        max_component_precursors=3,
        confine_competing_to_icsd=False,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False, add_pareto=True,
    ).dict(exclude_unset=True),
    SrNbO3=RecommendRoutesRequest(
        target_entry_id='mp-10339',
        confine_to_icsd=True,
        explicit_includes=['mp-561133'],
        add_elements=['C'],
        confine_to_stables=True,
        flexible_competition=0,
        temperature=1800,
        pressure=None,
        allow_gas_release=True,
        max_component_precursors=3,
        confine_competing_to_icsd=False,
        show_known_precursors_only=False,
        show_fraction_known_precursors=False,
        display_peroxides=False,
        display_superoxides=False, add_pareto=True,
    ).dict(exclude_unset=True)
)

if __name__ == "__main__":
    json.dump(requests, open('example_requests.json', 'w'))
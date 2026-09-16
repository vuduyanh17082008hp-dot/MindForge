from __future__ import annotations

import pytest
from pydantic import ValidationError

from mindforge.contracts import CognitiveBudget, CognitiveRoute, RouteMode


def valid_budget_values() -> dict[str, int]:
    return {
        'max_latency_ms': 500,
        'max_model_calls': 1,
        'max_tokens': 1000,
        'max_parallel_modules': 2,
        'max_tool_calls': 1,
        'max_reasoning_depth': 2,
    }


@pytest.mark.parametrize(
    'field_name',
    [
        'max_latency_ms',
        'max_model_calls',
        'max_tokens',
        'max_parallel_modules',
        'max_tool_calls',
        'max_reasoning_depth',
    ],
)
def test_budget_rejects_negative_values(field_name: str) -> None:
    values = valid_budget_values()
    values[field_name] = -1
    with pytest.raises(ValidationError):
        CognitiveBudget(**values)


@pytest.mark.parametrize('field_name', ['max_latency_ms', 'max_parallel_modules'])
def test_positive_budget_fields_reject_zero(field_name: str) -> None:
    values = valid_budget_values()
    values[field_name] = 0
    with pytest.raises(ValidationError):
        CognitiveBudget(**values)


@pytest.mark.parametrize('mode', [RouteMode.FAST, RouteMode.DEEP])
def test_route_supports_fast_and_deep(mode: RouteMode) -> None:
    route = CognitiveRoute(mode=mode)
    assert route.mode is mode


def test_route_supports_domain_specific_module_ids_without_hardcoding() -> None:
    route = CognitiveRoute(
        mode=RouteMode.DEEP,
        selected_modules=['education.tutor', 'legal_case-review'],
    )
    assert route.selected_modules == ['education.tutor', 'legal_case-review']
    assert all('dante' not in module for module in route.selected_modules)
    assert 'dante' not in str(CognitiveRoute.model_json_schema()).lower()


def test_route_rejects_duplicate_modules() -> None:
    with pytest.raises(ValidationError):
        CognitiveRoute(
            mode=RouteMode.DEEP,
            selected_modules=['shared_workspace', 'shared_workspace'],
        )


def test_budget_requires_all_limits() -> None:
    with pytest.raises(ValidationError):
        CognitiveBudget(max_latency_ms=500)


def test_budget_requires_integer_values() -> None:
    values = valid_budget_values()
    values['max_tokens'] = 1.5
    with pytest.raises(ValidationError):
        CognitiveBudget(**values)

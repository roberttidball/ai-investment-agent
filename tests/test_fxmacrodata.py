"""Offline analyst-tool and regional-context tests with synthetic fixtures."""

import asyncio
import json
from pathlib import Path

import pytest
from fxmacrodata_public import Result, list_operations

from src.tools.fxmacrodata import get_fxmacrodata_tools, regional_macro_evidence


class FixtureClient:
    def __init__(self):
        self.calls = []

    def execute(self, operation, arguments):
        self.calls.append((operation, arguments))
        return Result(
            operation,
            {
                "data": [
                    {
                        "val": 1.25,
                        "date": "2026-01-01",
                        "announcement_datetime": 1000000000,
                        "source_url": "https://example.org/release",
                    }
                ]
            },
        )


@pytest.mark.parametrize(
    "operation", list_operations(), ids=lambda operation: operation.name
)
def test_native_langchain_tool_consumes_every_operation(operation):
    client = FixtureClient()
    tools = {tool.name: tool for tool in get_fxmacrodata_tools(client)}
    tool = tools[f"fxmacrodata_{operation.name}"]
    assert tool.args_schema == operation.input_schema
    response = tool.invoke({})
    assert response["records"][0]["val"] == 1.25
    assert client.calls[0][0] == operation.name


def test_regional_brief_keeps_dates_and_each_currency():
    client = FixtureClient()
    result = asyncio.run(regional_macro_evidence("2026-01-03", "AUSTRALIA", client))
    assert 'currency="AUD"' in result and 'currency="NZD"' in result
    assert 'as_of="2026-01-03"' in result
    assert "example.org/release" in result
    assert client.calls[0][1]["end_date"] == "2026-01-03"
    assert client.calls[1][1]["end_date"] == "2026-01-17"


def test_unknown_region_does_not_substitute_us_data():
    client = FixtureClient()
    result = asyncio.run(regional_macro_evidence("2026-01-03", "UNKNOWN", client))
    assert 'status="unavailable"' in result
    assert client.calls == []


def test_errors_are_safe_and_do_not_become_available_evidence():
    class FailingClient:
        def execute(self, *args):
            raise RuntimeError("transport detail must not appear")

    result = asyncio.run(regional_macro_evidence("2026-01-03", "US", FailingClient()))
    assert "<result " not in result
    assert "transport detail" not in result


def test_configuration_errors_remain_private(monkeypatch):
    def unavailable_client():
        raise RuntimeError("configuration details must remain private")

    monkeypatch.setattr("src.tools.fxmacrodata.get_client", unavailable_client)
    response = get_fxmacrodata_tools()[0].invoke({})
    assert response["status"] == "unavailable"
    assert "configuration details" not in json.dumps(response)


def test_brief_uses_native_fetch_hook_and_news_registry(monkeypatch):
    import ast
    import sys
    import types

    source = Path(__file__).resolve().parents[1] / "src/macro_context.py"
    node = next(
        node
        for node in ast.parse(source.read_text(encoding="utf-8")).body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "_fetch_macro_raw"
    )

    class News:
        async def ainvoke(self, payload):
            return "News context"

    news = types.ModuleType("src.tools.news")
    news.get_macroeconomic_news = News()
    monkeypatch.setitem(sys.modules, "src.tools.news", news)

    async def official(*args):
        return "Official observations"

    monkeypatch.setattr("src.tools.fxmacrodata.regional_macro_evidence", official)
    namespace = {}
    exec(
        compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"),
        namespace,
    )
    assert (
        asyncio.run(namespace["_fetch_macro_raw"]("2026-01-03", "US"))
        == "News context\nOfficial observations"
    )
    registry = (source.parent / "tools/registry.py").read_text(encoding="utf-8")
    assert "*get_fxmacrodata_tools()" in registry

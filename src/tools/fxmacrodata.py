"""Structured macroeconomic evidence for the regional brief and analyst tools."""

from __future__ import annotations

import asyncio
import json
from datetime import date, timedelta
from html import escape
from typing import Any

from fxmacrodata_public import FXMacroDataClient, list_operations
from langchain_core.tools import StructuredTool

PROVIDER_URL = (
    "https://fxmacrodata.com/?utm_source=ai_investment_agent&utm_medium=integration"
    "&utm_campaign=open_source_integrations&utm_content=app"
)
# Multi-country buckets retain each currency label. No country's observations
# are substituted for another country's data or relabelled as regional facts.
REGION_CURRENCIES = {
    "US": ("USD",),
    "USA": ("USD",),
    "UNITED_STATES": ("USD",),
    "GLOBAL": ("USD",),
    "JAPAN": ("JPY",),
    "HONG_KONG": (),
    "CHINA": ("CNY",),
    "TAIWAN": (),
    "KOREA": (),
    "INDIA": (),
    "SEA": ("THB",),
    "AUSTRALIA": ("AUD", "NZD"),
    "CANADA": ("CAD",),
    "UK": ("GBP",),
    "EUROPE": ("EUR", "CHF", "NOK", "SEK", "DKK"),
    "LATAM": ("BRL", "PEN"),
}


def get_client() -> FXMacroDataClient:
    """Use the host's SecretStr configuration, outside tool arguments."""
    from src.config import config

    secret = config.fxmacrodata_api_key
    return FXMacroDataClient(api_key=secret.get_secret_value() if secret else "")


def _execute(
    operation: str, arguments: dict[str, Any], client: FXMacroDataClient | None = None
) -> dict[str, Any]:
    provider = client
    try:
        provider = provider or get_client()
        result = provider.execute(operation, arguments).as_dict()
        result["provider_url"] = PROVIDER_URL
        return result
    except Exception:
        return {
            "operation": operation,
            "status": "unavailable",
            "records": [],
            "error": "FXMacroData could not complete this request.",
        }
    finally:
        if client is None and provider is not None:
            provider.close()


def get_fxmacrodata_tools(
    client: FXMacroDataClient | None = None,
) -> list[StructuredTool]:
    """Return the complete public operation inventory in native LangChain form."""

    def make_handler(operation_name):
        def invoke(**arguments):
            return _execute(operation_name, arguments, client)

        return invoke

    tools = []
    for operation in list_operations():
        tools.append(
            StructuredTool.from_function(
                name=f"fxmacrodata_{operation.name}",
                description=f"FXMacroData: {operation.description}",
                args_schema=operation.input_schema,
                func=make_handler(operation.name),
            )
        )
    return tools


async def regional_macro_evidence(
    trade_date: str, region: str, client: FXMacroDataClient | None = None
) -> str:
    """Fetch dated official observations and a separately labelled event window.

    This is advisory context for the existing inspection/summarization path.
    No events are written to the portfolio shock store and no model-derived
    prediction is treated as market consensus or an observed release.
    """
    as_of = date.fromisoformat(trade_date)
    currencies = REGION_CURRENCIES.get(region.upper(), ())
    if not currencies:
        return '<fxmacrodata status="unavailable">No mapped currency for this region.</fxmacrodata>'
    sections = []
    for currency in currencies:
        for operation, arguments in (
            (
                "indicator_history",
                {
                    "currency": currency,
                    "indicator": "policy_rate",
                    "end_date": trade_date,
                    "limit": 5,
                },
            ),
            (
                "release_calendar",
                {
                    "currency": currency,
                    "start_date": trade_date,
                    "end_date": (as_of + timedelta(days=14)).isoformat(),
                },
            ),
        ):
            response = await asyncio.to_thread(_execute, operation, arguments, client)
            # Structured payload remains lossless inside a labelled source block.
            # escape() prevents source fields from breaking the evidence envelope.
            body = escape(json.dumps(response, ensure_ascii=False, default=str))
            if response.get("status") == "unavailable" or not response.get("records"):
                sections.append(
                    f'<fxmacrodata status="unavailable" currency="{currency}">{body}</fxmacrodata>'
                )
                continue
            sections.append(
                f'<result source="FXMacroData" currency="{currency}" '
                f'operation="{operation}" as_of="{trade_date}">{body}</result>'
            )
    return "\n".join(sections)

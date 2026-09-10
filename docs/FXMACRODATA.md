# FXMacroData for AI Investment Agent

Regional macro briefs receive dated policy-rate observations and a separately identified upcoming release window alongside existing news. The news analyst Toolkit exposes every public API/MCP operation. Source blocks enter the existing inspection and summarization path; these remain advisory context, not validated report evidence or portfolio shock records.

The core integration uses [FXMacroData](https://fxmacrodata.com/?utm_source=github&utm_medium=referral&utm_campaign=open_source_integrations&utm_content=ai_investment_agent_readme) always-free public USD endpoints and requires no API key, account or credit card. Public indicator history currently covers the most recent 90 days; catalogue and release-calendar access also work without a key. Optional authenticated coverage follows the API contract.

## Installation

The integration is included in the application dependencies. Install them using the project's normal command:

```sh
poetry install --with dev
```

Public USD data requires no API key. Optional authorization is configured below.

## Use

Optional FXMACRODATA_API_KEY is a host Pydantic SecretStr setting. Unsupported regional currencies remain unavailable. Multi-country buckets show each supported currency separately and do not pretend to cover all countries in a bucket. GLOBAL currently includes USD, explicitly labelled USD. The release window is the schedule retrieved at query time; historical as-of dates do not reconstruct publication vintages. No events are written to MacroEventsStore, which represents portfolio-detected shocks.

Start with `data_catalogue` and parameters `{"currency":"USD"}`, then `indicator_history` with `{"currency":"USD","indicator":"policy_rate","limit":5}` or `release_calendar` with `{"currency":"USD"}`. Agent tool names have an `fxmacrodata_` prefix. The operation catalogue includes exact required parameters and supported options.

The `data` field preserves the original public response; `records` is an additive table view. Keep source fields, assumed-time flags and timezone offsets when using the data. The API contract distinguishes official forecasts, market consensus and FXMacroData-generated outputs. Historical observation filters do not by themselves establish point-in-time vintage safety. Streaming is bounded by the client; it is not a persistent subscription.

[Public API reference](https://fxmacrodata.com/documentation/reference?utm_source=github&utm_medium=referral&utm_campaign=open_source_integrations&utm_content=ai_investment_agent_docs)

## Coverage

Every documented REST operation and listed hosted MCP tool is available through the native consumer above. Access requirements depend on the operation and currency. MCP tools, non-USD data and other protected datasets may require authorization; they are not required for the public USD baseline.

| Operation | Transport | Native consumer | Status |
| --- | --- | --- | --- |
| `health` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `ping` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `forex` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `intraday_reference_rates` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `fx_sources` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `fx_source_universe` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `data_catalogue` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `release_calendar` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `market_sessions` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `rate_differentials` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `curves` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `financial_prices` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `press_releases` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `risk_sentiment` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `factors` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `event_predictions` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `latest_announcements` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `indicator_history` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `cot` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `latest_commodities` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `commodities` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `announcement_changes` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `stream_events` | GET | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_ping` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_mcp_capabilities` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_mcp_auth_guide` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_subscribe_for_mcp_access` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_data_catalogue` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_risk_sentiment` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_macro_news` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_release_calendar` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_release_calendar_visual_artifact` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_event_predictions` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_latest_announcements` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_announcement_changes` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_press_releases` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_macro_factor` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_fx_reference_sources` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_fx_reference_universe` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_fx_intraday_reference_rates` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_rate_curve` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_rate_differentials` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_latest_commodities` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_forex` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_seasonality` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_indicator_query` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_plot_visual_artifact` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_indicator_visual_artifact` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_forex_visual_artifact` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_commodities_visual_artifact` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_cot_visual_artifact` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_policy_rate_differential_visual_artifact` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_macro_briefing_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_indicator_intel_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_pair_intel_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_macro_heatmap_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_policy_scenario_modeler_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_macro_war_room_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_event_impact_replay_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_quant_scenario_lab_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_known_at_time_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_macro_regime_classifier_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_release_risk_score_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_portfolio_risk_engine_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_fx_trade_setup_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_fx_backtest_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_macro_research_pack_task` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_market_sessions` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_cot_data` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_commodities` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_financial_prices` | MCP | `src/tools/fxmacrodata.py` | Implemented |
| `mcp_official_dataset_family` | MCP | `src/tools/fxmacrodata.py` | Implemented |

## Validation

Offline tests exercise every operation's native registration and record consumption plus the target-specific report, regional brief or economics route behavior.

```sh
python -m pytest tests/test_fxmacrodata.py -o addopts= -q -n 8 --dist load
```

These focused tests do not replace the target project's full CI gate. No live credentials or private datasets are fixtures.

## Attribution

Rob Tidball owns FXMacroData and maintains this adapter. Website links identify the provider; campaign parameters distinguish repository documentation visits from integration application visits. API/MCP requests have no campaign parameters, and the adapter sends no click telemetry.

# FPL LAB — UX Revision QA

## Static validation
- JavaScript syntax: PASS (`node --check app.js`)
- Python syntax: PASS (`server.py`, `tools/rebuild.py`)
- Duplicate HTML IDs: 0
- CSS braces: balanced
- Tactical tabs: Pitch / Matchup / XI
- Legacy visible wording “Football Intelligence”, “Data Through”, “Through GW”: removed from workspace copy

## Data / planner validation
- Full schedule: 380 fixtures / 38 gameweeks / 38 fixtures per club
- Official FDR mapping contract: club short names map uniquely across all 20 clubs
- Official FDR is fixture-specific, not a hardcoded team Home/Away table
- FDR range: 1–5
- Upcoming planner starts from the earliest GW that still contains an unplayed fixture
- Tie ranking uses the same rank for equal averages
- Custom FDR remains user-defined and separate from Official FPL

## Session validation
- Current autosave restores live Official FPL mode rather than freezing an empty official snapshot
- Named snapshots can preserve an exact Official FPL per-fixture snapshot
- Named custom snapshots preserve the custom ratings used at save time
- Overwrite confirmation and storage-error feedback retained

## Responsive QA
The revision layout was exercised at desktop and 390px during development before the final FDR logic-only patch. The final FDR patch changes data/state logic only and does not alter layout CSS.
- Mobile bottom navigation: retained
- Board filters: collapsed by default on <=760px
- Analysis Session: collapsed by default on <=760px
- Player Filters / Metric Library: collapsed by default on <=760px
- Tactical tabs: 3-column mobile layout
- Matrix/FDR tables: contained horizontal scrolling rather than document-level overflow
- XI: compact mobile pitch rules retained

## Environment note
A final full in-memory Chromium rerun can stall in this execution environment because the production data bundle is ~28 MB when inlined. Static checks and targeted logic tests passed after the final FDR patch; the layout itself was browser-tested before that logic-only patch.

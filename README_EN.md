# FPL LAB — Revision 2026/27

> This build includes the full UX revision for Overview, Tactical Board, FDR, Matchup XI, Player Intelligence and Chart Studio, with real Desktop/Mobile runtime QA. See `CHANGELOG_REVISION.md` and `QA_REVISION.md`.

# FPL LAB — Premier League Football Intelligence 2026/27

Local final candidate built from the supplied season archives. Indexed analytical data currently covers **GW1–GW9**, while the full **380-fixture** schedule is retained for future-fixture planning.

## Run

- Windows: extract the full ZIP and run `START_WINDOWS.bat`.
- macOS/Linux: run `sh START_MAC_LINUX.sh` inside the extracted folder.
- Manual: `python server.py --open` (Python 3.10+, no extra pip packages or npm required).

The app opens locally at `http://127.0.0.1:8765/`.

## Final feature set

- Overview with results, standings and FPL form context.
- Tactical Board with categorized filters, practical gameweek picker, stoppage-time-aware minute range, pitch zones, custom selection, event shapes, density/timeline, and internal workspace tabs.
- Matchup Intelligence with separate Shots / Bad touches / Crosses / Headers / Final-third-pass counts.
- League Vulnerability Matrix using **raw totals for the selected gameweeks**; every metric keeps its own independent rank regardless of which column is sorted.
- Crosses & Headers analysis: delivered/completed crosses, header shots, headers on target and header goals. It does not claim direct cross-to-header event attribution because the imported schema does not expose a verified event relation.
- Matchup XI Builder with real formations (3-4-3, 3-5-2, 4-3-3, 4-4-2, 4-5-1, 5-3-2, 5-4-1), eleven pitch slots, persisted reasons/context, replace/remove/role controls and unplaced overflow handling.
- User-defined Fixture Difficulty with Home/Away ratings, presets, edit history and a Next 3/5/6/8/10 planner over the full 380-fixture schedule.
- Player Intelligence with **146 usable metrics**, unified metric taxonomy, historical club attribution, search/filter/table/scatter/profile/comparison tools.
- Chart Studio with Performance Landscape, metric categories, club-crest themes, independent bubble size, user-selected 3–8 metric radar, corrected negative axes/bars, histogram/box logic and chart compatibility rules.
- Appearance system: Auto/Light/Dark/AMOLED, full workspace palettes, Solid/Transparent/Glass surfaces, opacity/blur controls and pitch logo/watermark branding.
- Analysis Sessions with autosave and named snapshots covering Tactical, Matchup, XI, FDR rating snapshot, Player Intelligence and Chart Studio state.
- Data Studio with provenance, coverage, local validated ZIP updates and high-coverage player-event linkage reporting.

## Packaged data

- 670 players.
- 90 completed indexed fixtures (GW1–GW9).
- 380 full-season schedule fixtures.
- 154,956 raw source event rows.
- 130,459 indexed analytical event rows.
- 146 usable metrics.
- 453/454 provider player IDs mapped.
- 99.95% linked indexed analytical event rows.

Key correctness rules include: own goals excluded from attacking shots, crosses excluded from pass totals, type 61 labelled Bad touch rather than total touches, header shots separated from aerial duels, period-based half logic, stoppage-time preservation, historical club mapping and field-aware aggregation. After excluding own goals correctly, raw event shot totals match match-level total shots on **180/180 team-sides** in the current indexed sample.

## Important interpretation notes

- Bad touch is not spatial total touches.
- Shot Sequence is a time-window context, not a verified possession chain unless a possession identifier is available.
- Some FPL snapshot fields are cumulative/as-of metrics, not selected-gameweek sums.
- Different sources may define assists or expected metrics differently; the product preserves source semantics instead of silently merging definitions.
- Local crest import skips images above 120 KB or when browser local storage is full.

## Data updates

For the first update after extracting this build, upload **both** the Performance and Events ZIP files in Data Studio. After a successful import, the local server caches both archives in `source_archives`, allowing later single-archive updates while reusing the cached counterpart. Validation must succeed before `data.js` is replaced, and the previous file is backed up.

See `QA_FINAL.md`, `CHANGELOG_FINAL.md`, and `REBUILD_INFO.json` for final validation details.

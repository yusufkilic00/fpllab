# FPL LAB — Phase 5 Correctness Core

Phase 5 prioritises data semantics, calculation correctness, deterministic rebuilds, chart logic and performance before the next UX pass.

## Data / Opta correctness

- Rebuilt `data.js` from the two user-supplied season archives.
- Preserves all 154,956 source event rows as source-quality metadata and indexes 130,459 supported analytical event rows.
- Separates Opta own-goal events (`type_id=16` + qualifier 28) from attacking shots.
- Splits crosses from passes (`type_id=1` + cross qualifier); crosses no longer inflate pass totals.
- Renames type 61 to **Bad touch** instead of pretending it represents all touches.
- Splits shot outcomes into goal, saved/on-target, blocked, missed and woodwork.
- Header shots are calculated from the shot body-part qualifier and exclude own goals.
- Uses provider player IDs with gameweek club history; ambiguous identities stay unmatched.
- Adds historical player-club mapping per gameweek.
- Removes all-null/non-aggregate fields from the usable metric catalogue.
- Aggregation is field-aware: sum, max, mean match rate, as-of snapshot, calculated or event-derived.
- `Top speed` now uses the maximum observed match value across the selected period.
- No longer requires exactly ten completed matches for a gameweek to be indexed.
- Detects duplicated logical source CSVs; identical duplicates are accepted, conflicting duplicates are rejected.

## Time / pitch logic

- Board time filters now use the actual maximum indexed minute (103 in this dataset), preserving stoppage time.
- Half comparison uses `period_id` rather than a minute `<45` shortcut.
- Flip-width now flips the plotted event coordinates and brush matching consistently, not just the lane label.
- Shot sequence lookup uses pre-indexed match/team/period events instead of repeated full-array searches.

## League Vulnerability Matrix

- Raw totals remain the basis for rankings, as requested.
- Ranks are calculated independently for every matrix metric from the **selected gameweeks only**.
- Sorting a different column changes row order but does not overwrite the other metric ranks.
- Changing the selected gameweeks recalculates every rank.
- Own goals are excluded from shot totals before ranking.
- Matrix leader is the true maximum even when the visible sort is ascending.
- Matchup event filter now labels type 61 honestly as **Bad touches**.

## Fixture Difficulty Planner

- The full 380-fixture schedule from the supplied performance archive is embedded separately from completed matches.
- Added upcoming planner windows: Next 3 / 5 / 6 / 8 / 10 gameweeks.
- Each fixture uses the opponent's user-defined Home/Away difficulty for the venue where that opponent plays.
- Teams reorder from easiest to hardest when the horizon or ratings change.
- Fixture count, total difficulty and average difficulty are shown separately so blanks/doubles are not silently treated as easy fixtures.
- Analysis snapshots now freeze the actual FDR rating values used at save time, not only the preset name.

## Player Intelligence / comparisons

- Player filtering and metric values respect the player's club in each selected gameweek, including transfers.
- Search now actually filters the player pool/table.
- Comparison metric category immediately exposes all available metrics in that category; search is optional.
- Comparison/player labels use the relevant selected-period club rather than blindly using the current club.
- Signed comparison bars now preserve negative direction.

## Chart Studio correctness

- Scatter/line/area domains are based on the data range instead of forcing zero into every chart.
- Bar charts support positive and negative values with an explicit zero baseline.
- Bubble charts use an independent size metric for Players, Teams and Matches.
- Radar uses 3–8 user-selected metrics and a same-position player cohort with minutes in the selected gameweeks.
- Histogram no longer forces zero into its domain.
- Box plots use standard 1.5×IQR whiskers and expose outliers.
- Donut refuses negative metrics and is disabled for match-row aggregation where part-to-whole semantics are undefined.
- “Heatmap” is labelled **2D density heatmap** to avoid implying a football-pitch heat map.
- Line/area use real gameweek values when a weekly log exists and do not automatically sum every player.

## Performance

- Added event indexes by team, gameweek and match/team/period.
- Matchup matrix scans only selected-gameweek indexed events and caches matrix/lane calculations.
- Startup renders only the active workspace.
- Snapshot restore renders only the restored active workspace instead of rebuilding every page.

## Dataset after rebuild

- 670 players
- 90 indexed completed fixtures (GW1–9)
- 380 fixtures in the full schedule
- 154,956 raw source event rows
- 130,459 indexed analytical event rows
- 146 usable metrics
- 453 / 454 provider player IDs mapped
- 99.95% linked indexed event rows

## Deferred to the next UX pass

The following known work is intentionally not hidden by this phase: filter category/size redesign, smoother gameweek picker, event-layer icon/shape system, moving Performance Landscape into Chart Studio, full colour-palette presets, real XI formations, Crosses↔Headers relationship view, matrix visual polish, and storage-failure notifications.

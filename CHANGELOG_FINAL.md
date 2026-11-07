# FPL LAB — Final Candidate Changelog

## Product / UX
- Left desktop navigation and mobile bottom navigation.
- Unified categorized filter system across Tactical Board, Player Intelligence, Comparison and Chart Studio.
- Practical gameweek picker: All, Last 3, Last 5, range and custom selections.
- Event Layers grouped and given distinct visual shapes.
- Tactical internal tabs prevent one extremely long analysis page.
- Full workspace palettes plus Solid / Transparent / Glass surface modes.
- Pitch branding controls with logo/wordmark/opacity.
- Team crest identity expanded to selectors, matrices, tables, XI and chart themes.

## Data correctness
- Provider-ID crosswalk replaces name-only event attribution.
- Historical player club membership is used for selected gameweeks.
- Own goals excluded from attacking shot populations and header-shot populations.
- Crosses no longer inflate pass totals.
- Type 61 labelled Bad touch rather than Total touches.
- Blocked shots and goalkeeper-save outcomes separated where qualifiers allow it.
- Period IDs drive half comparisons; stoppage time is retained to the actual maximum minute.
- Field-aware aggregation replaces a universal sum/average rule.
- Empty all-null metrics removed from the selectable catalogue.
- Missing, zero and not-applicable states kept distinct where the source supports that distinction.

## League Vulnerability Matrix
- Raw totals only, calculated inside the user-selected gameweeks.
- Independent rank per metric.
- Sorting one metric only reorders rows; it never rewrites other metric ranks.
- Rank population excludes own goals from attacking shot totals.
- Improved alignment, sticky reading aids, club identity and rank badges.

## Matchup Intelligence
- Separate activity families: Shots, Bad touches, Crosses, Headers and Final-third passes.
- Player drill-down preserves source context and can add directly to Matchup XI.
- Crosses & Headers panel added with delivered/completed crosses, header shots, on-target headers and header goals.
- Aggregate relationship is shown without inventing direct cross-to-header event linkage.

## Matchup XI
- Real formation selector: 3-4-3, 3-5-2, 4-3-3, 4-4-2, 4-5-1, 5-3-2, 5-4-1.
- Eleven actual pitch slots.
- Formation persisted in local workspace state and snapshots.
- Natural-role reset, role changes, remove, replace-next and unplaced overflow handling.

## Fixture Difficulty
- User-defined Home/Away ratings and presets retained.
- Full 380-fixture schedule used for planning.
- Next 3/5/6/8/10 horizon selector.
- Dynamic easiest-to-hardest ranking based on the active user ratings.
- Analysis snapshots store a copy of the ratings used at save time.

## Charts / comparisons
- Performance Landscape moved into Chart Studio.
- Comparison categories immediately expose their metrics without requiring text search.
- Radar uses selectable 3–8 metrics and position-aware comparison cohorts.
- Bubble chart gets an independent size metric.
- Negative bars/axes, histogram domains, box-plot whiskers and donut compatibility corrected.
- Club crest chart theme added.

## Performance / persistence
- Indexed event lookups reduce repeated full-event scans.
- Snapshot restore avoids rebuilding unrelated hidden workspaces.
- Analysis Session state expanded and persisted.
- First data import now explicitly requires both source archives if no cached counterpart exists.

## Final polish
- Initial Data Studio metric count corrected to 146.
- Local crest import capped at 120 KB per image to avoid silently exhausting browser local storage; skipped/storage-failed images are reported.
- Responsive containment added so wide analytical surfaces scroll inside their own wrappers instead of forcing page-level horizontal scrolling.

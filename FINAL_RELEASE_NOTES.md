# FPL LAB — Final Review Build 2026/27

This package consolidates the work completed through the correctness and UX passes into one reviewable product build.

## Included
- Left-side desktop navigation and responsive mobile navigation.
- Unified filter categories, practical gameweek presets/range/custom selection, and event-layer grouping with distinct visual symbols.
- Workspace themes, full palettes, glass/transparency controls, and pitch branding/watermark controls.
- Corrected Opta event semantics used by the analytical layer, including own-goal shot exclusion, pass/cross separation, period-aware halves, stoppage-time support, and historical player club attribution.
- League Vulnerability Matrix with independent raw-total ranks per metric for the selected gameweeks.
- Matchup Intelligence with selectable event families and persistent player-selection context.
- Matchup XI Builder with selectable formations (3-4-3, 3-5-2, 4-3-3, 4-4-2, 4-5-1, 5-3-2, 5-4-1), pitch slots, replace/remove controls, and saved selection reasons.
- Crosses & Headers context panel: crosses delivered/completed, header shots, headers on target, header goals, lane counts, and player leaders. Cross/header counts are independent aggregates; no unverified event-to-event assist relation is claimed.
- Custom Fixture Difficulty presets with separate Home/Away ratings and an upcoming-fixture planner using the full season schedule.
- Player Intelligence metric categories and comparison metric browser.
- Chart Studio correctness/UX improvements including custom radar metrics, negative-value handling, bubble sizing, team/crest themes, and Performance Landscape presets.
- Data Studio linkage/coverage reporting and local update workflow.

## Data scope in this build
Analytical match/event coverage is based on the imported completed data currently indexed in the project. The full league schedule is retained for future-fixture planning.

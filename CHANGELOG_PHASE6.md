# FPL LAB — Phase 6: UX & Consistency Pass

Phase 6 focuses on making the existing analysis tools feel like one coherent product. The Phase 5 data/correctness layer is retained unchanged.

## Tactical Board
- Added a compact internal workspace navigation: Pitch / Matchup / Matchup XI / Fixture Difficulty / Sequences.
- Rebuilt Tactical filters into collapsible categories: Teams & context, Gameweeks & time, Event layers, Event details, Pitch view.
- Added active-filter chips and a single Clear filters action.
- Replaced the long GW chip row with All / Last 3 / Last 5, From–To range controls, and a Custom GW picker.
- Grouped Event Layers into Possession, Finishing, Defending, and Duels & discipline.
- Event layers now use distinct visual symbols (arrow, arc, target, diamond, triangle, square, hex, etc.) in controls and legends.
- Event-specific controls are disabled when their related layer is not selected.
- Unified control heights, radii, spacing, and label hierarchy.

## League Vulnerability Matrix
- Center-aligned headers and values for quicker scanning.
- Added clearer row hover behavior and sticky team column treatment.
- Preserved independent Raw Total rank badges for every metric; sorting a column does not alter other metric ranks.
- Improved column emphasis and team identity presentation.

## Player Intelligence
- Reorganized filters into Player scope, Gameweeks, and Metric library sections.
- Added a reusable metric taxonomy with category tabs and search.
- Metric library now shows grouped category cards instead of a flat wall of metrics.
- Removed Performance Landscape from Player Intelligence to reduce duplication.

## Player Comparison
- Category selection now immediately displays the metrics in that category; search is optional and only narrows the current selection.
- Added grouped candidate metrics and a separate selected-metrics area.
- Added club identity to comparison player cards.
- Standardized filter and control sizing.

## Chart Studio
- Moved Performance Landscape into Chart Studio.
- Added a metric-category control to Performance Landscape.
- Added chart presets for player landscape, team landscape, player radar, and gameweek trend.
- Reorganized every chart card into Chart / Metrics / Appearance / Gameweeks sections.
- Player metrics are category-aware inside Chart Studio.
- Added visual themes including Club crest theme, FPL LAB, and Minimal.
- Club crest theme uses club identity in supported charts; player/team historical club attribution from Phase 5 is retained.
- Performance Landscape can send its current setup directly to the main chart builder.

## Appearance
- Added full workspace palettes: Graphite, Midnight, Carbon, Violet, and Slate.
- Workspace palettes change background/surface/border systems, not only the accent colour.
- Existing Dark / Light / AMOLED, Solid / Transparent / Glass, opacity, blur, and pitch-branding settings remain available.

## Data integrity
- `data.js` is byte-for-byte unchanged from Phase 5.
- Phase 6 is a UX/layout layer over the corrected Phase 5 calculations.

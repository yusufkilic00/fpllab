# Responsive & Visual QC — 2026-11-07

Tested the production UI at 1440×900, 1024×768, 768×1024, 390×844 and 360×800, including Home, Tactical Board, Player Intelligence, Chart Studio and Data Studio. Tactical Board Pitch/Matchup/XI were also checked.

## Fixed
- Player Filters inherited a legacy six-column grid on desktop/laptop, creating a large empty panel and clipping gameweek controls around 1024px. The filter clusters now stack full-width and use their own responsive inner grids.
- Tactical Board Event Layers had nested-grid overflow: the outer category grid was forced to three columns while each category also required multiple minimum-width event buttons. Categories now stack full-width and their internal button grids handle responsive columns.
- Mobile/tablet bottom navigation now provides a full 70px touch area above safe-area insets.
- Small faint labels received a modest contrast increase in dark and light modes.
- Missing local player photos now fall back to the styled player placeholder instead of an unstyled glyph.

## Verified
- No document-level horizontal overflow at the tested widths.
- Mobile initial load collapses Analysis Session, Player Filters and Metric Library as intended, keeping the main workspace above the fold.
- Home and Data Studio scale cleanly from desktop to 360px.
- Wide analytical tables/matrices remain intentionally horizontally scrollable inside their own containers.
- JavaScript has no syntax errors and the tested UI produced no page-level runtime exceptions.

## Remaining performance note
Production data is split into Cloudflare-safe files, but `data-loader.js` currently downloads every indexed gameweek before starting the app. The current 9-GW JSON set is about 26.9 MiB uncompressed and about 3.4 MiB with typical gzip compression. This is acceptable for an initial release but should become on-demand/lazy gameweek loading as the season grows toward GW38.

## Asset note
107 of the 670 current player records do not have a matching local WebP file in `assets/players`. They now render a consistent fallback, but adding the missing licensed player images would improve visual completeness. Club crests currently have a built-in text fallback when the external crest source is unavailable.

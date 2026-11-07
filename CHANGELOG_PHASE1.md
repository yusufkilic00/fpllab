# FPL LAB 2026/27 — Phase 1 UI & Appearance Update

## Implemented

- Moved primary workspace navigation to a fixed left sidebar on desktop.
- Preserved the existing mobile bottom navigation for smaller screens.
- Reorganized Tactical Board filters into a top toolbar above the pitch/results.
- Reorganized Player Intelligence filters into a top toolbar above the table/plots.
- Kept all original filter/control IDs so the existing analysis logic continues to use the same controls.
- Added a new appearance system with:
  - Auto / Light / Dark / AMOLED modes.
  - Emerald, Cyan, Blue, Violet, Amber, Rose, Slate and Monochrome accents.
  - Solid / Transparent / Glass surface styles.
  - Surface opacity slider.
  - Glass blur slider.
  - Appearance persistence via localStorage.
- Added configurable pitch branding:
  - Off.
  - Wordmark.
  - Logo.
  - Logo + wordmark.
  - Watermark opacity control.
- Added responsive behavior so the sidebar yields to mobile navigation on smaller screens.
- Fixed the Player Profile snapshot hardcode from GW9 to the latest available gameweek dynamically.

## Not changed in this phase

The underlying Matchup Intelligence calculations, event-player matching, Chart Studio calculation logic, Fixture Difficulty Builder and Matchup XI Builder are intentionally left for the next implementation phases. This phase focuses on layout/appearance while preserving the current analysis logic.

## Validation performed

- JavaScript syntax check (`app.js`, `updates.js`).
- Python syntax check for the local server.
- HTML parsed and checked for duplicate IDs.
- Confirmed all original filter IDs required by the existing JavaScript remain present.

A full visual browser QA pass should still be performed on the target machine/browser after extraction.

# FPL LAB — UX Revision

## Overview
- Removed repeated “Football Intelligence” wording.
- Removed “Data Through GW09” / “Through GW09” from the Overview and league table.
- Gameweek Hub now covers all 38 gameweeks, with previous/next controls, fixture dates/times and completed results when indexed.
- The selected GW is not repeated below every fixture.

## Tactical Board
- Tactical navigation is now Pitch / Matchup / XI.
- Pitch filters are one collapsible panel instead of multiple numbered panels.
- Pitch keeps a compact team selector; Team + Opponent context lives in Matchup.
- Event sequences now live under Pitch.
- Fresh workspaces default to the last 3 indexed GWs.

## Matchup / FDR
- Fixture Difficulty is integrated into Matchup.
- Official FPL FDR is the default and is loaded per fixture from the public FPL fixtures feed (`team_h_difficulty` / `team_a_difficulty`) and cached locally.
- If no verified official cache is available offline, the UI says so instead of inventing an “official” rating.
- Custom FDR remains optional via Edit FDR, with user-defined Home/Away team ratings.
- Upcoming horizon uses − / + controls (1–15 GWs).
- Difficulty cells are colour coded.
- Tied planner averages share the same rank.
- Partial gameweeks remain in the upcoming window while they still contain unplayed fixtures.
- Named analysis snapshots preserve the exact FDR snapshot used; current autosave remains live.

## Matchup XI
- Manual formation selection removed.
- Manual position editing removed.
- Player positions are fixed to FPL roles.
- Formation is selected automatically from the current XI composition.
- Desktop and mobile pitch layouts are more compact.
- Clear XI requires confirmation.

## Player Intelligence / Comparison
- Player filters are one collapsible panel.
- Metric Library is a separate collapsible panel.
- Large metric categories are visually split into metric families without adding another click level.
- Comparison controls use compact shared sizing.

## Chart Studio
- Controls use the same compact sizing system as the other workspaces.
- Performance Landscape remains in Chart Studio.
- Existing chart correctness and club-crest themes are preserved.

## Sessions / Mobile
- Analysis Session is collapsible and defaults closed on mobile.
- Snapshot overwrite requires confirmation.
- Storage failures surface an explicit message.
- Mobile filters and Metric Library default closed.
- Tactical navigation is a three-button mobile grid.
- Pitch/XI/Comparison/Charts received mobile-specific sizing rather than desktop-only scaling.

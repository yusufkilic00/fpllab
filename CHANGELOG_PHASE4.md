# FPL LAB — Phase 4

## Analysis Session
- Added a persistent current-workspace autosave stored locally in the browser.
- Added named analysis snapshots that can be saved, loaded, and deleted.
- Session snapshots preserve Tactical Board teams, gameweeks, event layers, pitch zone/brush, minute and outcome filters, Matchup Intelligence event families, Matchup XI, Player Intelligence filters/comparisons, and Chart Studio configuration.
- Appearance remains a global preference and is intentionally not tied to an analysis snapshot.
- Starting a new analysis resets analysis context while retaining appearance and fixture-difficulty presets.

## Custom Fixture Difficulty
- Added user-defined 1–5 ratings for every club, separately for Home and Away.
- Added multiple named presets.
- Added Save As, Reset to 3, and Delete preset actions.
- Added a recent-change log per preset with timestamp, club, venue, and old/new values.
- Ratings are explicitly labelled as user-defined and are not official FPL difficulty values.
- The active fixture-difficulty preset is remembered inside Analysis Session snapshots.

## Persistence
- Added local storage keys for live workspace autosave, named analysis snapshots, and fixture-difficulty presets.
- Existing Phase 1–3 appearance, Matchup XI, matchup event filters, data-quality, and chart fixes are preserved.

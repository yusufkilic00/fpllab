# FPL LAB — QA summary

Verified in a local Chromium smoke test on **1366×850** and **390×850** viewports:

- Opened all five pages without uncaught JavaScript exceptions.
- Overview: 10 fixture rows and 20 league-table rows from source fixtures.
- Tactical Board: 20-club matchup table, zone selection changed event count from 4,808 to 1,811 for the default team; matchup drawer displayed both directions.
- Player Intelligence: 670 players eligible on initial scatter, 30 initially visible table rows and functional navigation.
- Chart Studio: Dashboard mode displayed four independent charts.
- Data Studio: source import file controls present.
- No root-level horizontal overflow at 1366 or 390 pixels.
- Rebuild of original ZIPs succeeded: **90 fixtures, 670 players, 130,459 events, 155 metrics**; 408 event-linked player IDs.
- Invalid event ZIP upload returned HTTP **422**; SHA-256 digest of working `data.js` before and after was unchanged.
- JS syntax check passed (`node --check app.js`); Python server and dataset rebuild script compiled.

Additional matchup checks previously passed: sort matrix column, expand and collapse a team, switch conceded/taken, and update gameweek selection on desktop and mobile.

**Scope:** These are automated smoke and integration checks, not a guarantee that every filter combination, visual detail, licensed external logo or future data-update format has been validated. The remote crest images were not reachable from the sandbox test environment; offline fallback and manual ZIP importing were left in place. External automatic data updates are not configured.

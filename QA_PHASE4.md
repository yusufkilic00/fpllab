# Phase 4 QA notes

Checks completed:
- JavaScript syntax: `node --check app.js` passes.
- Python server/rebuild syntax: `python -m py_compile` passes.
- HTML ID uniqueness: no duplicate IDs detected.
- New Analysis Session and Fixture Difficulty controls exist in the DOM.
- Local server smoke test: `/api/status`, `index.html`, and `app.js` return HTTP 200.
- CSS brace counts are balanced after Phase 4 additions.

Important manual browser checks to perform after download:
1. Change Tactical Board filters, refresh, and confirm current workspace is restored.
2. Save a named snapshot, change filters, reload the named snapshot, and confirm the saved state returns.
3. Add players to Matchup XI, save a snapshot, and verify the XI and reasons return.
4. Create a fixture-difficulty preset, change Home/Away values, refresh, and verify persistence.
5. Load a snapshot that references a different fixture-difficulty preset and verify the preset switches correctly.
6. Test responsive layout on mobile-width browser windows.

The environment could serve the app locally, but a full Chromium visual run was not completed because the headless Chromium process did not terminate reliably in this container.

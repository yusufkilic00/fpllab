# Phase 3 QA

- `app.js` passes `node --check`.
- `index.html` parses without duplicate IDs.
- Required Phase 3 DOM anchors are present.
- Event archive sanity counts: 2,476 shots; 6,368 ball-touch events; 3,173 crosses; 412 header-shot events; 17,160 successful passes ending in the final third.
- 170 linked players have at least one header-shot event in the current archive.
- Local HTTP smoke test verifies the updated index, application JavaScript, CSS and data bundle are served.
- Headless Chromium visual QA is not available in this container because Chromium hangs on the environment's DBus/browser sandbox setup; browser visual review should still be done on the target machine.

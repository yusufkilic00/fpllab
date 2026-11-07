# FPL LAB — Phase 5 QA

## Static checks

- `node --check app.js`: PASS
- `python -m py_compile tools/rebuild.py`: PASS
- Duplicate HTML IDs: 0
- Rebuild from the exact two supplied ZIPs: PASS
- Rebuild determinism: rebuilt `data.js` SHA-256 matched the packaged `data.js` byte-for-byte.

## Dataset checks

- Full fixture schedule: 380
- Indexed completed fixtures: 90
- Raw source event rows: 154,956
- Indexed analytical event rows: 130,459
- Linked indexed event rows: 99.95%
- Usable metrics: 146
- All-zero-coverage metrics exposed: 0
- Own-goal events separated: 12
- Correct attacking shots after separation: 2,464
- Shot outcomes partition correctly: 231 goals + 493 saves/on-target + 766 blocked + 934 missed + 40 woodwork = 2,464
- Header shots: 411
- Passes: 83,946; Crosses: 3,173 stored separately
- Bad touches: 6,368, explicitly not labelled total touches

## Cross-source validation

After excluding own goals from attacking shots, Opta event shot totals matched the supplied official match-total shot figures for all **180 team-sides** in the 90 completed fixtures.

## Runtime browser checks

Chromium was run with the production HTML/CSS/JS loaded in-memory because the environment blocks local URL navigation.

PASS:
- Home and Tactical Board initialise without JavaScript page errors.
- Board min/max controls expose minute 103.
- League Vulnerability Matrix renders 20 clubs.
- Independent rank badges remain unchanged when sorting another matrix metric.
- Changing selected gameweeks recalculates the raw-total ranks.
- Historical club filter test: Baleba appears for Brighton in GW1, does not appear for Man Utd in GW1, and appears for Man Utd from GW2.
- Comparison category “Attacking” immediately exposed 23 available attacking metrics without entering a search term.
- FDR planner renders 20 clubs and Next 3 changes the displayed horizon from GW10–14 to GW10–12.
- Bubble size is a separate finite metric for all 20 team rows in the test.
- Donut match-source semantic guard is active.
- New-analysis reset returns the time window to 0–103.
- Analysis snapshot restore measured about 80 ms in the browser test, with no page error.
- Radar exposes a 3–8 metric multi-select.

## Known limits / next QA

- Attack-direction normalization is still not independently verified from an external orientation flag; the UI therefore retains the manual flip-width control.
- “Bad touch” is intentionally not presented as total spatial touches. Building true spatial touches requires a defensible event-definition model.
- Mean match percentage fields are labelled as mean match rates; they are not represented as reconstructed weighted season percentages when reliable denominators are unavailable.
- UX/layout issues documented in the product audit remain for the next phase and are not claimed as fixed by this correctness release.

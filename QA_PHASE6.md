# Phase 6 QA

## Static checks
- `node --check app.js`: PASS
- HTML duplicate IDs: none
- Required Phase 6 DOM anchors present: PASS
- Phase 5 `data.js` SHA-256 preserved: `39f900ab41b3477e77aadfb6a94524539ecafdeacd5499307d6f2610af28d4a9`

## Headless Chromium interaction test
The production HTML/CSS plus the real Phase 5 `data.js` and Phase 6 `app.js` were loaded in Chromium in-memory.

Observed results:
- No JavaScript page errors.
- Tactical Board filter sections: 5.
- Event Layer groups: 4; event buttons: 15.
- Gameweek `Last 3` preset correctly reports 3 selected GWs.
- Tactical sub-navigation hides Pitch while showing Matchup correctly.
- Vulnerability Matrix rows: 20.
- Matrix rank badges rendered: 240 for the active three event families / lane columns.
- Player metric category tabs: 11.
- Performance Landscape absent from Player Intelligence and present in Chart Studio.
- Selecting a Comparison category displayed 23 candidate metrics immediately without requiring a search.
- Chart Studio control hierarchy rendered 3 filter sections plus the separate Gameweeks section.
- Club crest visual theme selected and available.
- Workspace palette switch to Midnight updated the document theme state successfully.

## Scope
This phase intentionally does not change Phase 5 data calculations. Formation-based XI layout and the deeper Cross → Header relationship model remain later work.

# FPL LAB — Phase 3

## Matchup Intelligence
- Added independent event-family filters for Shots, Touches, Crosses, Headers, and successful Final-third passes.
- Matrix columns are now generated from the selected event families instead of being fixed to shots/crosses.
- Player lane rankings show each selected event family separately; event families are no longer collapsed into one unexplained number.
- Header analysis uses shot body-part qualifier `15` only. Aerial duels are not classified as headers.
- Header shots count once in the lane activity total even when both Shots and Headers are selected, while the separate metric counts remain visible.
- Added caching for player lane calculations to keep repeated matchup exploration responsive.

## Matchup XI Builder
- Add a linked player directly from any matchup lane.
- Persists XI locally across refreshes.
- Stores the matchup reason, opponent context, lane and selected gameweeks for every player.
- Supports up to 11 players.
- Supports remove, clear XI, role changes (GK / DEF / MID / FWD), and a “Replace next” workflow when the XI is full.
- Existing XI selections remain visible while changing matchup teams, gameweeks and event filters.

## Notes
- Matchup activity describes recorded event locations across selected gameweeks; it is not an xG model or a prediction.
- Final-third passes are successful passes whose end-x coordinate is in the final third.
- Left/right interpretation still depends on provider orientation and the existing Flip width control.

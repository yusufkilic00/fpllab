# FPL LAB — Phase 2

## Data quality
- Replaced per-event name-only matching with a provider `player_id` crosswalk.
- Uses each player's club in the relevant gameweek, so transfers do not break historical linkage.
- Ambiguous identities remain unmatched instead of being guessed.
- Event-player linkage improved to 453 of 454 provider IDs in the current GW1–GW9 dataset.
- 130,393 of 130,459 indexed event rows are player-linked (99.95%). Of the 66 unlinked rows, only four carry the unmatched named identity `R. Angulo`; the rest do not provide a usable player identity for the supported event row.
- Added Data Studio coverage cards and team-level linkage watchlist.
- Event-derived missing data is no longer blindly converted to zero where coverage is absent.

## Chart Studio correctness
- Line and Area charts now plot a selected player/team series across gameweeks instead of summing all players/teams by default.
- Weekly FPL totals use gameweek logs where available; snapshot-only metrics are labelled as snapshots.
- Radar now compares different metrics for one selected player/team and normalizes them to population percentiles.
- Bar charts show entity names and values and support Top 10 / 14 / 20 / 50 / All.
- Empty or unavailable values remain missing rather than being silently plotted as zero.

## Matchup linkage
- Matchup player rows now use the linked FPL player ID embedded in each event first, with legacy name matching only as a fallback.

## Validation
- `tools/rebuild.py` compiles successfully.
- `app.js` passes `node --check`.
- Dataset shape validated: 670 players, 90 fixtures, 130,459 events, 155 metrics, no malformed event rows, and no invalid linked player IDs.

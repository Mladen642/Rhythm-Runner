# Architecture

## The game

The whole game is one HTML5 canvas, 320 by 180 pixels, scaled up with nearest-neighbour filtering. The engine is
`game/engine.js`; `game/play.html` loads the chapter data for `play.html?ch=N`, then the meSpeak library, then the engine.

- **Clock.** Everything is timed by `songTime()`, derived from the Web Audio clock while the chapter track plays. Note
  positions, hit windows and boss events are all in song seconds, so frame drops never shift the timing. Tempo surge
  stretches this clock together with the music's playback rate.
- **Chart.** Each chapter is one continuous audio file with five stages. The chart is a list of notes
  (`t` time, `l` lane, `k` kind, `s` stage, `d` hold length) built from the melody and drum events of each song.
- **Judging.** Perfect within 50 ms, Great within 100 ms, Good within 150 ms (`WP`, `WG`, `WO` at the top of the
  engine). Misses drain the 16-segment groove meter; every groove loss is scaled by `BOSS_DMG` (0.85) through `dmgScale()`.
- **Boss mechanics.** `pickMechs()` enumerates every valid trio for the chapter's budget and picks one at random;
  `scheduleMechs()` places windowed mechanics on bar-aligned slots; `applyMechs()` rewrites the boss chart for the run.
  The tables `MECH`, `COST`, `MINCH` and `BUDGET` near the top of the mechanics code control all of it.
- **Voices.** Lines are spoken with the system text-to-speech when Chromium offers voices; otherwise the bundled
  meSpeak engine (`game/lib`) synthesises them and plays them through the game's own mixer.
- **Saves.** Progress is kept in `localStorage`, one key per chapter (`rr_ch<N>_prog`, plus `rr_ch<N>_best` and the
  shared `rr_offset`); the start page reads it to show stars. The storage belongs to the `app://game` origin and the
  app's data folder (`~/.config/Rhythm Runner`), so keep the protocol host and `productName` unchanged or saves are lost.

## Data

`game/data/chN.json` holds everything for chapter N in play order: stages and their worlds, the chart, sprites (as
paths into `assets/img`), dialogue lines, comics, the cast for duets and helpers, and boss data. `songs` maps track keys
to MP3 files in `assets/audio`; `loops` gives the loop lengths of the title and pause music.

Sprite files are named by a hash of their content, so shared sprites are stored once. Audio files keep the original
chapter numbers from the generator scripts (see the table in [tools/README.md](../tools/README.md)).

The start page `game/index.html` carries its own small data block (font, chapter cards, title-screen worlds) inline.

## Desktop shell

`desktop/main.js` registers an `app://` protocol that serves the game folder (Chromium blocks `fetch()` on `file://`
URLs), opens one fullscreen window without a menu bar, and toggles fullscreen on F11 and Alt+Enter. During development it
serves `../game`; electron-builder copies that folder into the package as `web`, and the packaged app serves it from there.

# Architecture

## The game

The whole game is one HTML5 canvas, 320 by 180 pixels, scaled up with nearest-neighbour filtering. The engine lives in
`tools/chapter_engine.html`; the app build turns it into `engine.js` plus a small loader page (`play.html`).

- **Clock.** Everything is timed by `songTime()`, derived from the Web Audio clock while the chapter track plays. Note
  positions, hit windows and boss events are all in song seconds, so frame drops never shift the timing. Tempo surge
  stretches this clock together with the music's playback rate.
- **Chart.** Each chapter is one continuous audio file with five stages. The chart is a list of notes
  (`t` time, `l` lane, `k` kind, `s` stage, `d` hold length) built from the melody and drum events of each song.
- **Judging.** Perfect within 50 ms, Great within 100 ms, Good within 150 ms. Misses drain the 16-segment groove meter.
  Boss stages scale damage by `BOSS_DMG` (0.85).
- **Boss mechanics.** `pickMechs()` enumerates every valid trio for the chapter's budget and picks one at random;
  `scheduleMechs()` places windowed mechanics on bar-aligned slots; `applyMechs()` rewrites the boss chart for the run.
  The tables `MECH`, `COST`, `MINCH` and `BUDGET` near the top of the mechanics code control all of it.
- **Voices.** Lines are spoken with the system text-to-speech when the browser offers voices; otherwise the bundled
  meSpeak engine synthesises them and plays them through the game's own mixer.
- **Saves.** Progress is kept in `localStorage`, one key per chapter (`rr_ch<N>_prog`); the start page reads it to
  show stars.

## Data

`build/web/data/chN.json` holds everything for chapter N: stages and their worlds, the chart, sprites (as paths into
`assets/img`), dialogue lines, comics, the cast for duets and helpers, and boss data. `songs` maps track keys to MP3
files in `assets/audio`; `loops` gives the loop lengths of the title and pause music.

## Building the app

`tools/app_build.py` reads the chapter data (stored under the original chapter numbers), renumbers it into play order,
repaints the "next chapter" teaser in each ending comic, extracts every embedded image into `assets/img` (named by a
hash of its content, so shared sprites are stored once), copies the music, and writes `engine.js` and `play.html`.
`tools/app_start.py` generates the start page.

## Desktop shell

`desktop/main.js` registers an `app://` protocol that serves the web build (Chromium blocks `fetch()` on `file://`
URLs), opens one fullscreen window without a menu bar, and toggles fullscreen on F11 and Alt+Enter. electron-builder
packages it as an AppImage.

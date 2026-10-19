# Releasing

1. Update the version in `desktop/package.json`.
2. Build the AppImage:

   ```bash
   cd desktop && npm install && npm run dist
   ```

3. Start `desktop/dist/RhythmRunner-<version>-x86_64.AppImage` once and play a few seconds of a chapter.
4. On GitHub, open Releases, choose "Draft a new release", create a tag named after the version (such as `0.2.0`, like
   the existing `0.1.0`), and attach `desktop/dist/RhythmRunner-<version>-x86_64.AppImage`.

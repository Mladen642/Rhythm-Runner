# Releasing

1. Update the version in `desktop/package.json`.
2. Rebuild the game and the AppImage:

   ```bash
   cd tools && python3 app_build.py && python3 app_start.py
   cd ../desktop && npm install && npm run dist
   ```

3. Pack the web build:

   ```bash
   cd ../build && cp -r web rhythm-runner-web && zip -r rhythm-runner-web-<version>.zip rhythm-runner-web && rm -r rhythm-runner-web
   ```

4. On GitHub, open Releases, choose "Draft a new release", create a tag such as `v<version>`, and attach
   `desktop/dist/RhythmRunner-<version>-x86_64.AppImage` and `build/rhythm-runner-web-<version>.zip`.

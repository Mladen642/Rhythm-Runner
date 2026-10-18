// Rhythm Runner desktop shell.
// Serves the web build through an app:// protocol (so fetch() works for chapter data and music)
// and opens one fullscreen game window.
const { app, BrowserWindow, protocol, net, Menu } = require('electron');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true } }]);
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
// Character voices prefer the system text-to-speech; on Linux, Chromium only reaches speech-dispatcher with this switch.
// When no system voices exist, the game falls back to the bundled meSpeak engine.
if (process.platform === 'linux') app.commandLine.appendSwitch('enable-speech-dispatcher');

// Packaged builds carry the game in ./web; during development it lives in ../build/web.
const packaged = path.join(__dirname, 'web');
const root = fs.existsSync(packaged) ? packaged : path.join(__dirname, '..', 'build', 'web');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280, height: 800, minWidth: 660, minHeight: 420, fullscreen: true,
    backgroundColor: '#000000', title: 'Rhythm Runner', autoHideMenuBar: true,
    icon: path.join(root, 'icon.png'),
    webPreferences: { contextIsolation: true, sandbox: true },
  });
  win.webContents.on('before-input-event', (e, input) => {
    const toggle = input.type === 'keyDown' && (input.key === 'F11' || (input.alt && input.key === 'Enter'));
    if (toggle) { win.setFullScreen(!win.isFullScreen()); e.preventDefault(); }
  });
  win.loadURL('app://game/index.html');
}

app.whenReady().then(() => {
  protocol.handle('app', (req) => {
    const rel = decodeURIComponent(new URL(req.url).pathname).replace(/^\/+/, '') || 'index.html';
    const file = path.normalize(path.join(root, rel));
    if (!file.startsWith(root)) return new Response('Not found', { status: 404 });
    return net.fetch(pathToFileURL(file).toString());
  });
  Menu.setApplicationMenu(null);
  createWindow();
});
app.on('window-all-closed', () => app.quit());

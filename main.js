const { app, BrowserWindow, shell } = require('electron');
const path = require('path');

// Optional Squirrel (Windows) events: ignore if module is absent.
// This avoids the dev-time crash "Cannot find module 'electron-squirrel-startup'".
let squirrelStartup = false;
try { squirrelStartup = require('electron-squirrel-startup'); } catch { squirrelStartup = false; }
if (squirrelStartup) { app.quit(); }

function createWindow () {
  const win = new BrowserWindow({
    width: 1240,
    height: 900,
    backgroundColor: '#0b0f14',
    show: false,
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    titleBarStyle: 'hiddenInset'
  });
  win.once('ready-to-show', () => win.show());
  win.removeMenu();
  win.loadFile('index.html');
  win.webContents.setWindowOpenHandler(({ url }) => {
    require('electron').shell.openExternal(url);
    return { action: 'deny' };
  });
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (require('electron').BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
let win;
function create() {
  const area = screen.getPrimaryDisplay().workArea;
  win = new BrowserWindow({
    width: 180, height: 190,
    x: Math.max(area.x, area.x + Math.floor(area.width * 0.35)),
    y: Math.max(area.y, area.y + Math.floor(area.height * 0.35)),
    frame: false, transparent: true, backgroundColor: '#00000000',
    resizable: false, skipTaskbar: true, alwaysOnTop: true, hasShadow: false,
    webPreferences: { contextIsolation: true, nodeIntegration: false, preload: path.join(__dirname, 'preload.js') }
  });
  win.setAlwaysOnTop(true, 'screen-saver');
  win.loadFile(path.join(__dirname, 'index.html'));
}
app.whenReady().then(create);
ipcMain.handle('get-desktop-info', () => ({
  bounds: screen.getPrimaryDisplay().workArea,
  position: win && !win.isDestroyed() ? win.getPosition() : [120, 120]
}));
ipcMain.on('move-window', (_, x, y) => {
  if (win && !win.isDestroyed()) {
    const area = screen.getDisplayNearestPoint({ x: Math.round(x), y: Math.round(y) }).workArea;
    const [w, h] = win.getSize();
    const safeX = Math.max(area.x, Math.min(Math.round(x), area.x + area.width - w));
    const safeY = Math.max(area.y, Math.min(Math.round(y), area.y + area.height - h));
    win.setPosition(safeX, safeY);
  }
});
ipcMain.on('quit-app', () => app.quit());
app.on('window-all-closed', () => app.quit());

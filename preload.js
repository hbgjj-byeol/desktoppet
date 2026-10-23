const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('hamsterAPI', {
  move: (x, y) => ipcRenderer.send('move-window', x, y),
  desktopInfo: () => ipcRenderer.invoke('get-desktop-info'),
  quit: () => ipcRenderer.send('quit-app')
});

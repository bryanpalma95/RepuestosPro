import { app, BrowserWindow, shell } from 'electron';
import { randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createApi } from '../server/src/app.js';
import { SecurityStore } from '../server/src/store.js';
import { createScheduledBackup } from '../tools/backup/lib.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
let apiServer;
let store;
const DESKTOP_PORT = 17873;
const APP_VERSION = '0.10.0-beta.1';
const desktopDataDirectory = app.isPackaged ? join(dirname(process.execPath), 'data') : join(root, 'var', 'desktop-data');
mkdirSync(join(desktopDataDirectory, 'profile'), { recursive: true });
app.setPath('userData', join(desktopDataDirectory, 'profile'));

function portableDataDirectory() {
  return desktopDataDirectory;
}

function loadSecret(dataDirectory) {
  const secretFile = join(dataDirectory, '.session-secret');
  if (!existsSync(secretFile)) writeFileSync(secretFile, randomBytes(48).toString('base64'), { flag: 'wx' });
  return readFileSync(secretFile, 'utf8').trim();
}

async function startApi() {
  const dataDirectory = portableDataDirectory();
  mkdirSync(dataDirectory, { recursive: true });
  store = new SecurityStore(join(dataDirectory, 'repuestospro.sqlite'));
  for (const migration of ['0001_foundations.sql', '0002_workshop_core.sql', '0002_security_hardening.sql', '0003_local_workshop_state.sql']) {
    store.migrate(join(root, 'database', 'migrations', 'sqlite', migration));
  }
  try {
    createScheduledBackup({
      source: join(dataDirectory, 'repuestospro.sqlite'),
      destination: join(dataDirectory, 'backups'),
      schemaVersion: '0003_local_workshop_state',
      retention: 14
    });
  } catch (error) {
    console.error('No fue posible crear el respaldo automático:', error.message);
  }
  apiServer = createApi({ store, sessionSecret: loadSecret(dataDirectory), staticRoot: root, localMode: true });
  await new Promise((resolveListen, reject) => {
    apiServer.once('error', reject);
    apiServer.listen(DESKTOP_PORT, '127.0.0.1', resolveListen);
  });
  return DESKTOP_PORT;
}

async function createWindow() {
  const port = await startApi();
  const window = new BrowserWindow({
    width: 1360,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    show: false,
    autoHideMenuBar: true,
    title: `RepuestosPro Taller — v${APP_VERSION}`,
    backgroundColor: '#0f172a',
    webPreferences: { contextIsolation: true, nodeIntegration: false, sandbox: true },
  });
  window.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('http://127.0.0.1:')) return { action: 'allow' };
    shell.openExternal(url);
    return { action: 'deny' };
  });
  await window.loadURL(`http://127.0.0.1:${port}/taller.html`);
  window.show();
}

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) app.quit();
else {
  app.on('second-instance', () => {
    const window = BrowserWindow.getAllWindows()[0];
    if (window) { if (window.isMinimized()) window.restore(); window.focus(); }
  });
  app.whenReady().then(createWindow).catch((error) => {
    console.error(error);
    app.quit();
  });
  app.on('window-all-closed', () => app.quit());
  app.on('before-quit', () => {
    apiServer?.close();
    store?.close();
  });
}

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false
        }
    });

    win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

ipcMain.on('message', (event, arg) => {
    console.log(arg); // Prints "Hello from the renderer process!"
});

ipcMain.on('run-python', (event, arg) => {
    const python = spawn('python', ['python_script.py', arg]);
    python.stdout.on('data', (data) => {
        event.reply('python-output', data.toString());
    });
    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
});

ipcMain.on('run-python-mic', (event) => {
    const python = spawn('python', ['python_script.py', '--mic']);
    python.stdout.on('data', (data) => {
        event.reply('python-output', data.toString());
    });
    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
});

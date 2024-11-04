const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    win.loadFile('index.html');

    // Handle background tasks or communication with the Python script here
    // For example, you might use a child process to execute the Python script:
    const { spawn } = require('child_process');
    const pythonProcess = spawn('python', ['python_script.py']);

    pythonProcess.stdout.on('data', (data) => {
        // Handle output from the Python script
        console.log(`Python script output: ${data}`);
        // Send the output to the renderer process (your HTML/CSS/JS) using IPC
    });
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
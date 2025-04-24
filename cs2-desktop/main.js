const { app, BrowserWindow, ipcMain, Menu, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const installDependencies = require('./install-deps');

// Keep a global reference of the window object to avoid garbage collection
let mainWindow;
let backendProcess = null;
let mongoProcess = null;

// Path to the backend directory
const backendPath = path.join(__dirname, 'backend');
const frontendBuildPath = path.join(__dirname, 'build');

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            // Allows the renderer process to use require() and process
            enableRemoteModule: true
        },
        icon: path.join(__dirname, 'build', 'favicon.ico')
    });

    // Load the index.html of the app
    mainWindow.loadFile(path.join(frontendBuildPath, 'index.html'));

    // Open the DevTools in development mode
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }

    // Emitted when the window is closed
    mainWindow.on('closed', function () {
        mainWindow = null;
    });

    // Build application menu
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Reload Data',
                    click() {
                        mainWindow.webContents.send('reload-data');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Exit',
                    click() {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                { role: 'reload' },
                { role: 'forceReload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'resetZoom' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { type: 'separator' },
                { role: 'togglefullscreen' }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'About CS2 Esports Tracker',
                    click() {
                        dialog.showMessageBox(mainWindow, {
                            title: 'About CS2 Esports Tracker',
                            message: 'CS2 Esports Tracker Desktop',
                            detail: 'Version 1.0.0\nA desktop application for tracking CS2 esports matches and betting opportunities.',
                            buttons: ['OK']
                        });
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

function startBackend() {
    // Check if Python is installed
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';

    // Start MongoDB if needed
    if (process.platform !== 'win32') {  // Skip on Windows, assuming MongoDB is installed as a service
        mongoProcess = spawn('mongod', ['--dbpath', path.join(os.tmpdir(), 'cs2_mongodb')]);
        
        mongoProcess.stdout.on('data', (data) => {
            console.log(`MongoDB stdout: ${data}`);
        });
        
        mongoProcess.stderr.on('data', (data) => {
            console.error(`MongoDB stderr: ${data}`);
        });
        
        mongoProcess.on('error', (error) => {
            console.error(`Failed to start MongoDB: ${error}`);
            // Proceed anyway, in case MongoDB is already running as a service
        });
    }

    // Give MongoDB a moment to start
    setTimeout(() => {
        // Start the backend server
        console.log('Starting backend server...');
        backendProcess = spawn(pythonCommand, [path.join(backendPath, 'server.py')], {
            cwd: backendPath,
            env: { ...process.env, PYTHONUNBUFFERED: '1' }
        });

        backendProcess.stdout.on('data', (data) => {
            console.log(`Backend stdout: ${data}`);
        });

        backendProcess.stderr.on('data', (data) => {
            console.error(`Backend stderr: ${data}`);
        });

        backendProcess.on('close', (code) => {
            console.log(`Backend process exited with code ${code}`);
        });

        backendProcess.on('error', (err) => {
            console.error('Failed to start backend:', err);
            dialog.showErrorBox(
                'Backend Error',
                `Failed to start the backend server. Make sure Python is installed and all dependencies are met.\n\nError: ${err.message}`
            );
        });
    }, 2000);
}

// This method will be called when Electron has finished initialization
app.whenReady().then(async () => {
    // Check if we're running the installer
    if (process.argv.includes('--install-deps')) {
        await installDependencies();
        app.quit();
        return;
    }
    
    // Check if this is the first run and we need to install dependencies
    const userDataPath = app.getPath('userData');
    const configPath = path.join(userDataPath, 'config.json');
    
    if (!fs.existsSync(configPath)) {
        // First run, show welcome screen and install dependencies
        createWindow();
        mainWindow.loadFile(path.join(__dirname, 'build', 'welcome.html'));
        
        dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'First Run Setup',
            message: 'Welcome to CS2 Esports Tracker!',
            detail: 'This appears to be your first time running the application. We need to install some dependencies before you can start using it. This may take a few minutes.',
            buttons: ['Install Now', 'Cancel'],
            defaultId: 0,
            cancelId: 1
        }).then(result => {
            if (result.response === 0) {
                // User clicked "Install Now"
                mainWindow.webContents.send('installation-status', 'Installing dependencies...');
                
                installDependencies().then(success => {
                    if (success) {
                        dialog.showMessageBox({
                            type: 'info',
                            title: 'Installation Complete',
                            message: 'Dependencies installed successfully!',
                            detail: 'You can now start using CS2 Esports Tracker.',
                            buttons: ['Start Application']
                        }).then(() => {
                            mainWindow.loadFile(path.join(frontendBuildPath, 'index.html'));
                            startBackend();
                        });
                    } else {
                        dialog.showMessageBox({
                            type: 'error',
                            title: 'Installation Failed',
                            message: 'Failed to install dependencies.',
                            detail: 'Please try running the application again or install the dependencies manually.',
                            buttons: ['Close']
                        }).then(() => {
                            app.quit();
                        });
                    }
                });
            } else {
                // User clicked "Cancel"
                app.quit();
            }
        });
    } else {
        // Normal startup
        createWindow();
        startBackend();
    }

    app.on('activate', function () {
        // On macOS it's common to re-create a window when the dock icon is clicked
        if (mainWindow === null) createWindow();
    });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
});

// When app is about to quit, kill the backend process
app.on('will-quit', () => {
    if (backendProcess) {
        console.log('Killing backend process...');
        if (process.platform === 'win32') {
            // On Windows
            spawn('taskkill', ['/pid', backendProcess.pid, '/f', '/t']);
        } else {
            // On Linux/macOS
            backendProcess.kill('SIGTERM');
        }
    }

    if (mongoProcess) {
        console.log('Killing MongoDB process...');
        if (process.platform === 'win32') {
            // On Windows
            spawn('taskkill', ['/pid', mongoProcess.pid, '/f', '/t']);
        } else {
            // On Linux/macOS
            mongoProcess.kill('SIGTERM');
        }
    }
});

// Handle IPC events from the renderer process
ipcMain.on('restart-backend', () => {
    if (backendProcess) {
        if (process.platform === 'win32') {
            // On Windows
            spawn('taskkill', ['/pid', backendProcess.pid, '/f', '/t']);
        } else {
            // On Linux/macOS
            backendProcess.kill('SIGTERM');
        }
        backendProcess = null;
        setTimeout(startBackend, 1000);
    } else {
        startBackend();
    }
});
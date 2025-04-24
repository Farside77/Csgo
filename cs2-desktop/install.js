const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log('Installing CS2 Esports Tracker Desktop...');

// Platform-specific installations
const isPlatformWindows = process.platform === 'win32';
const isPlatformMac = process.platform === 'darwin';
const isPlatformLinux = process.platform === 'linux';

// Install Python dependencies
console.log('Installing Python dependencies...');
try {
    // Determine Python command (python or python3)
    const pythonCommand = isPlatformWindows ? 'python' : 'python3';
    
    // Check if Python is installed
    try {
        execSync(`${pythonCommand} --version`);
    } catch (error) {
        console.error(`${pythonCommand} not found. Please install Python 3.8 or higher.`);
        process.exit(1);
    }
    
    // Install pip packages
    execSync(`${pythonCommand} -m pip install -r "${path.join(__dirname, 'backend', 'requirements.txt')}"`);
    console.log('Python dependencies installed successfully.');
} catch (error) {
    console.error('Failed to install Python dependencies:', error.message);
    process.exit(1);
}

// MongoDB setup
console.log('Setting up MongoDB...');
try {
    const mongoDbPath = path.join(os.tmpdir(), 'cs2_mongodb');
    
    // Create MongoDB data directory if it doesn't exist
    if (!fs.existsSync(mongoDbPath)) {
        fs.mkdirSync(mongoDbPath, { recursive: true });
    }
    
    // Windows: Check if MongoDB is installed or offer to download
    if (isPlatformWindows) {
        try {
            execSync('mongod --version');
            console.log('MongoDB is already installed.');
        } catch (error) {
            console.log('MongoDB is not installed or not in PATH.');
            console.log('Please install MongoDB from https://www.mongodb.com/try/download/community');
            console.log('After installation, restart this installer.');
            process.exit(1);
        }
    }
    
    // macOS: Check if MongoDB is installed via Homebrew or offer to install
    if (isPlatformMac) {
        try {
            execSync('mongod --version');
            console.log('MongoDB is already installed.');
        } catch (error) {
            console.log('MongoDB is not installed or not in PATH.');
            console.log('Installing MongoDB via Homebrew...');
            
            try {
                execSync('brew --version');
                execSync('brew tap mongodb/brew');
                execSync('brew install mongodb-community');
                console.log('MongoDB installed successfully via Homebrew.');
            } catch (brewError) {
                console.error('Failed to install MongoDB via Homebrew:', brewError.message);
                console.log('Please install MongoDB from https://www.mongodb.com/try/download/community');
                console.log('After installation, restart this installer.');
                process.exit(1);
            }
        }
    }
    
    // Linux: Check if MongoDB is installed or offer to install
    if (isPlatformLinux) {
        try {
            execSync('mongod --version');
            console.log('MongoDB is already installed.');
        } catch (error) {
            console.log('MongoDB is not installed or not in PATH.');
            
            if (fs.existsSync('/etc/debian_version')) {
                console.log('Detected Debian/Ubuntu. Installing MongoDB...');
                try {
                    execSync('sudo apt-get update');
                    execSync('sudo apt-get install -y mongodb');
                    console.log('MongoDB installed successfully via apt.');
                } catch (aptError) {
                    console.error('Failed to install MongoDB via apt:', aptError.message);
                    console.log('Please install MongoDB manually and restart this installer.');
                    process.exit(1);
                }
            } else {
                console.log('Please install MongoDB appropriate for your Linux distribution.');
                console.log('After installation, restart this installer.');
                process.exit(1);
            }
        }
    }
    
    console.log('MongoDB setup completed.');
} catch (error) {
    console.error('Error setting up MongoDB:', error.message);
    process.exit(1);
}

console.log('CS2 Esports Tracker installation completed successfully!');
console.log('To start the application, run: npm start');
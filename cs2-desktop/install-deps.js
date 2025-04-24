const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const { app } = require('electron');

module.exports = async function installDependencies() {
  console.log('Installing dependencies for CS2 Esports Tracker...');
  
  const isWindows = process.platform === 'win32';
  const isMac = process.platform === 'darwin';
  const isLinux = process.platform === 'linux';
  
  try {
    // MongoDB data directory
    const mongoDataDir = path.join(app.getPath('userData'), 'mongodb-data');
    if (!fs.existsSync(mongoDataDir)) {
      fs.mkdirSync(mongoDataDir, { recursive: true });
    }
    
    // Install Python dependencies
    try {
      const pythonCommand = isWindows ? 'python' : 'python3';
      const pip = isWindows ? 'pip' : 'pip3';
      
      // Check Python
      let hasPython = false;
      try {
        execSync(`${pythonCommand} --version`);
        hasPython = true;
      } catch (err) {
        console.log('Python not found. Checking alternative command...');
        try {
          if (isWindows) {
            execSync('python3 --version');
            hasPython = true;
          } else {
            execSync('python --version');
            hasPython = true;
          }
        } catch (err2) {
          console.log('Python is not installed or not in PATH');
        }
      }
      
      if (hasPython) {
        // Get app resources path
        const resourcesPath = process.env.NODE_ENV === 'development' 
          ? path.join(__dirname, 'backend') 
          : path.join(process.resourcesPath, 'backend');
        
        // Install requirements
        const requirementsPath = path.join(resourcesPath, 'requirements.txt');
        console.log(`Installing Python packages from ${requirementsPath}...`);
        
        try {
          execSync(`${pip} install -r "${requirementsPath}"`, { stdio: 'inherit' });
          console.log('Python dependencies installed successfully.');
        } catch (pipErr) {
          console.error('Failed to install with pip, trying with --user flag');
          execSync(`${pip} install --user -r "${requirementsPath}"`, { stdio: 'inherit' });
        }
      }
    } catch (error) {
      console.error('Error installing Python dependencies:', error);
    }
    
    // Write configuration
    try {
      const configPath = path.join(app.getPath('userData'), 'config.json');
      const config = {
        mongoDbPath: mongoDataDir,
        installDate: new Date().toISOString()
      };
      
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
      console.log(`Configuration saved to ${configPath}`);
    } catch (error) {
      console.error('Error writing configuration:', error);
    }
    
    console.log('Dependency installation completed.');
    return true;
  } catch (error) {
    console.error('Error during dependency installation:', error);
    return false;
  }
};
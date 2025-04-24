/**
 * Script to build the Windows installer
 * Run this with: node build-installer.js
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const appName = 'CS2 Esports Tracker';
const distPath = path.join(__dirname, 'dist');
const buildConfig = {
  win: true,
  mac: false,
  linux: false
};

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  underscore: '\x1b[4m',
  blink: '\x1b[5m',
  reverse: '\x1b[7m',
  hidden: '\x1b[8m',
  
  fg: {
    black: '\x1b[30m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    white: '\x1b[37m'
  },
  
  bg: {
    black: '\x1b[40m',
    red: '\x1b[41m',
    green: '\x1b[42m',
    yellow: '\x1b[43m',
    blue: '\x1b[44m',
    magenta: '\x1b[45m',
    cyan: '\x1b[46m',
    white: '\x1b[47m'
  }
};

console.log(`${colors.bright}${colors.fg.cyan}======================================${colors.reset}`);
console.log(`${colors.bright}${colors.fg.white}  Building ${appName} Installer${colors.reset}`);
console.log(`${colors.bright}${colors.fg.cyan}======================================${colors.reset}\n`);

// 1. Clean the dist folder if it exists
if (fs.existsSync(distPath)) {
  console.log(`${colors.fg.yellow}Cleaning previous builds...${colors.reset}`);
  try {
    fs.rmdirSync(distPath, { recursive: true });
    console.log(`${colors.fg.green}✓ Previous builds cleaned${colors.reset}\n`);
  } catch (err) {
    console.error(`${colors.fg.red}✗ Error cleaning previous builds: ${err.message}${colors.reset}\n`);
  }
}

// 2. Install dependencies
console.log(`${colors.fg.yellow}Installing dependencies...${colors.reset}`);
try {
  execSync('npm install', { stdio: 'inherit' });
  console.log(`${colors.fg.green}✓ Dependencies installed${colors.reset}\n`);
} catch (err) {
  console.error(`${colors.fg.red}✗ Error installing dependencies: ${err.message}${colors.reset}\n`);
  process.exit(1);
}

// 3. Build the application
console.log(`${colors.fg.yellow}Building application...${colors.reset}`);
try {
  // Create build commands based on configuration
  const buildCommands = [];
  if (buildConfig.win) buildCommands.push('npm run build:win');
  if (buildConfig.mac) buildCommands.push('npm run build:mac');
  if (buildConfig.linux) buildCommands.push('npm run build:linux');
  
  // Execute build commands
  for (const cmd of buildCommands) {
    console.log(`${colors.dim}> ${cmd}${colors.reset}`);
    execSync(cmd, { stdio: 'inherit' });
  }
  
  console.log(`${colors.fg.green}✓ Application built successfully${colors.reset}\n`);
} catch (err) {
  console.error(`${colors.fg.red}✗ Error building application: ${err.message}${colors.reset}\n`);
  process.exit(1);
}

// 4. Show output location
console.log(`${colors.bright}${colors.fg.cyan}======================================${colors.reset}`);
console.log(`${colors.fg.green}✓ ${colors.bright}Build completed successfully!${colors.reset}`);
console.log(`${colors.fg.white}Installer location: ${colors.bright}${distPath}${colors.reset}`);
console.log(`${colors.bright}${colors.fg.cyan}======================================${colors.reset}\n`);

// 5. Offer to run the installer
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});

readline.question(`${colors.fg.yellow}Would you like to run the installer now? (y/n) ${colors.reset}`, (answer) => {
  if (answer.toLowerCase() === 'y') {
    console.log(`${colors.fg.cyan}Starting installer...${colors.reset}`);
    try {
      // Find the installer in the dist folder
      const files = fs.readdirSync(distPath);
      const installerFile = files.find(file => file.endsWith('.exe'));
      
      if (installerFile) {
        const installerPath = path.join(distPath, installerFile);
        console.log(`${colors.dim}> ${installerPath}${colors.reset}`);
        
        // On Windows, use start to open the installer
        if (process.platform === 'win32') {
          execSync(`start "" "${installerPath}"`, { stdio: 'inherit' });
        } else {
          console.log(`${colors.fg.yellow}Automated launch only supported on Windows.${colors.reset}`);
          console.log(`${colors.fg.white}Please manually run the installer at: ${colors.bright}${installerPath}${colors.reset}`);
        }
      } else {
        console.log(`${colors.fg.red}No installer found in ${distPath}${colors.reset}`);
      }
    } catch (err) {
      console.error(`${colors.fg.red}Error running installer: ${err.message}${colors.reset}`);
    }
  }
  
  readline.close();
});
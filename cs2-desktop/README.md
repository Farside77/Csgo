# CS2 Esports Tracker Desktop

A desktop application for tracking CS2 esports matches, making predictions, and tracking betting opportunities.

## Features

- View upcoming CS2 matches
- See predictions for match outcomes and scores
- Calculate EV (Expected Value) for betting opportunities
- Track bets and analyze performance
- Filter matches by team, event, status, and more

## For End Users: Installation

### Using the Installer (Recommended)

1. Download the latest installer from the releases page
2. Run the installer and follow the on-screen instructions
3. Launch the application from your desktop or start menu

The installer will automatically check for and help you install required dependencies (Python and MongoDB).

### System Requirements

- Windows 10/11, macOS 10.14+, or Ubuntu 18.04+ (64-bit)
- 4GB RAM minimum, 8GB recommended
- 500MB disk space + additional space for MongoDB
- Internet connection for fetching match data

## For Developers: Building from Source

### Prerequisites

- Node.js 14+ (https://nodejs.org)
- npm 6+ (comes with Node.js)
- Python 3.8+ (https://python.org)
- MongoDB 4.4+ (https://mongodb.com)
- Git (https://git-scm.com)

### Setup Development Environment

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cs2-esports-tracker-desktop.git
   cd cs2-esports-tracker-desktop
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the application in development mode:
   ```
   npm run dev
   ```

### Building the Installer

#### Quick Build (Windows)

Run the build-installer.bat script:
```
build-installer.bat
```

#### Quick Build (macOS/Linux)

Run the build-installer.sh script:
```
./build-installer.sh
```

#### Manual Build Process

1. Install development dependencies:
   ```
   npm install
   ```

2. Build the application installer:
   
   **For Windows:**
   ```
   npm run build:win
   ```
   
   **For macOS:**
   ```
   npm run build:mac
   ```
   
   **For Linux:**
   ```
   npm run build:linux
   ```

3. The installer will be created in the `dist` folder

## Application Structure

- `main.js` - Main Electron process
- `preload.js` - Preload script for secure IPC
- `build/` - Frontend files
- `backend/` - Python backend
  - `server.py` - FastAPI server
  - `requirements.txt` - Python dependencies
- `resources/` - Additional resources for the app
- `install-deps.js` - Dependency installer
- `installer.nsh` - NSIS installer customization

## Usage Guide

### Main Interface

- **Refresh Matches:** Click the "Refresh Matches" button to fetch the latest matches
- **Restart Backend:** If you encounter any issues with the backend, click "Restart Backend"
- **Filtering:** Use the filters at the top to find specific matches
- **Placing Bets:** Click on the "Bet on [Team]" button and enter your bet amount
- **Stats:** View your betting performance statistics at the right side of the application

### First Run Experience

On first launch, the application will:
1. Check if required dependencies are installed
2. Guide you through installing any missing dependencies
3. Set up the MongoDB database
4. Load the main application interface

## Technologies Used

- **Electron** - Desktop application framework
- **React** - UI framework (embedded in Electron renderer)
- **FastAPI** - Python-based backend API
- **MongoDB** - NoSQL database for match and bet storage
- **Python** - Backend logic and prediction algorithms
- **electron-builder** - Packaging and installer creation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
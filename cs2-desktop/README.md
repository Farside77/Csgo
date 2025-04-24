# CS2 Esports Tracker Desktop

A desktop application for tracking CS2 esports matches, making predictions, and tracking betting opportunities.

## Features

- View upcoming CS2 matches
- See predictions for match outcomes and scores
- Calculate EV (Expected Value) for betting opportunities
- Track bets and analyze performance
- Filter matches by team, event, status, and more

## Installation

### Prerequisites

- Node.js (v14 or later)
- Python 3.8 or later
- MongoDB

### Installation Steps

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cs2-esports-tracker-desktop.git
   cd cs2-esports-tracker-desktop
   ```

2. Install dependencies:
   ```
   npm install
   node install.js
   ```

   This will install both Node.js and Python dependencies.

### Starting the Application

**Windows:**
```
start.bat
```

**macOS/Linux:**
```
./start.sh
```

Or directly using npm:
```
npm start
```

## Building the Application

To build a distributable version:

```
npm run dist
```

This will create platform-specific distributables in the `dist` folder.

## Usage

- **Refresh Matches:** Click the "Refresh Matches" button to fetch the latest matches
- **Restart Backend:** If you encounter any issues with the backend, click "Restart Backend"
- **Filtering:** Use the filters at the top to find specific matches
- **Placing Bets:** Click on the "Bet on [Team]" button and enter your bet amount
- **Stats:** View your betting performance statistics at the right side of the application

## Technologies Used

- Electron - Desktop application framework
- React - UI framework
- FastAPI - Backend API
- MongoDB - Database
- Python - Backend logic and predictions

## License

MIT
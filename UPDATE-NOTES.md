# CS2 Esports Tracker - v1.1.0 Update Notes

## New Features: Advanced LAN Performance Analysis

We're excited to introduce a significant improvement to the CS2 Esports Tracker prediction model, focusing on LAN vs. online performance differentiation:

### 🏆 LAN Performance Weighting

* **LAN performances now weighted 3x higher** than online performances
* **Rich visual analysis** showing each team's LAN and online win rates
* **Time decay factors** for recency - recent performances matter much more
* **Competitive context awareness** - upcoming LAN matches prioritize LAN history

### 🔄 Roster Stability Analysis

* **Roster change tracking** to account for team stability
* **Automatic adjustment** of predictions based on how recently teams changed players
* **Historical performance filtering** based on current roster

### 📈 Enhanced Match Analysis

* **New "Performance Factors" section** showing detailed team statistics
* **LAN/online indicators** for upcoming matches
* **Roster stability percentage** indicating team cohesion
* **Days since last roster change** for context

### 🎮 Behind the Scenes

* **Monte Carlo simulation** for more accurate map score prediction
* **Exponential decay model** with 90-day half-life for performance history
* **Head-to-head analysis** with LAN/online and recency weighting
* **Component weighting system** that adjusts for match context

## How This Helps You Find Value Bets

This update significantly improves prediction accuracy by accounting for:

1. **Tournament context** - Teams often perform differently at major LAN events vs. online qualifiers
2. **Roster stability** - Teams with recent changes are appropriately downgraded until they prove themselves
3. **Psychological factors** - LAN performance better indicates how teams handle pressure
4. **Network variable elimination** - Removes the impact of ping and network conditions on analysis

## Using the New Features

1. **Match Analysis:** Click the "Analysis" button on any match to see detailed performance data
2. **Filters:** Use the new filter options to focus on LAN vs online matches
3. **Betting Recommendations:** The EV calculations now account for LAN/online differences

## Technical Details

For those interested in the technical implementation, please refer to the detailed documentation in `/app/README-LAN-PERFORMANCE.md`

## Upcoming Features

We're working on:
* **Player performance tracking** for even more detailed analysis
* **Map veto simulation** for improved pre-match prediction
* **Historical tournament placement** weighting
* **Machine learning model** trained on historical match data

We value your feedback! Let us know how these new features are working for you.

Happy betting!

---
*CS2 Esports Tracker Team*
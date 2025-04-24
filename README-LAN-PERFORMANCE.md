# LAN vs Online Performance Analysis in CS2 Esports Tracker

## Overview

The CS2 Esports Tracker now includes advanced analysis of LAN (Local Area Network) vs. online performances, with time-decay factors and roster stability analysis. This document explains the implementation and how it improves prediction accuracy.

## Why LAN Performance Matters

In professional Counter-Strike, LAN performances are generally considered more indicative of a team's true skill level for several reasons:

1. **No latency issues**: All players compete on the same network with minimal ping
2. **Psychological factors**: Players must perform under pressure with a live audience
3. **No remote advantages**: Eliminates concerns about remote cheating or unfair setups
4. **Tournament significance**: Major tournaments are typically LAN events

## Implementation Details

### 1. Match Type Classification

Each match is classified as either:
- **LAN**: Typically major tournaments where teams play in person
- **Online**: Matches played remotely over the internet

### 2. Performance Weighting

The prediction model weights performances as follows:

- **LAN matches**: Weighted 3x higher than online matches
- **Recent matches**: Exponential time decay with a 90-day half-life
- **Post-roster change matches**: Double weighted if played after the most recent roster change

### 3. Roster Stability Analysis

The model tracks roster changes and calculates a stability factor:
- Teams with very recent changes (< 30 days) are heavily penalized
- Stability increases gradually and normalizes after 180 days
- Matches played with the current roster are weighted more heavily

### 4. Head-to-Head Analysis

When analyzing direct matchups between teams:
- Recent matchups get higher weight (90-day half-life)
- LAN matchups are weighted 3x higher than online ones
- Only matchups after both teams' recent roster changes are double-weighted

## The Mathematical Model

For each team, we calculate:

1. **Weighted LAN win rate**:
   ```
   LAN_win_rate = weighted_LAN_wins / total_weighted_LAN_matches
   ```

2. **Weighted online win rate**:
   ```
   online_win_rate = weighted_online_wins / total_weighted_online_matches
   ```

3. **Combined weighted win rate**:
   ```
   weighted_win_rate = (LAN_win_rate * 3 + online_win_rate) / 4
   ```

The time weight for each match uses exponential decay:
   ```
   time_weight = 2^(-days_ago / 90)
   ```

Roster stability is calculated as:
   ```
   roster_stability = min(1.0, days_since_roster_change / 180)
   ```

## How This Improves Predictions

1. **More realistic performance assessment**: By emphasizing LAN performance, the model better captures true team skill levels without network variables
2. **Adaptation to roster changes**: Teams that have recently changed players are appropriately downgraded until they prove themselves
3. **Recency bias**: Recent performances matter much more than older ones
4. **Context-awareness**: For upcoming LAN events, past LAN performance is weighted even more heavily

## Using the Feature

When viewing match analysis, you'll now see:
- Whether the match is LAN or online
- Each team's LAN and online win rates
- Roster stability percentages
- Days since last roster change
- Additional performance factors used in prediction

This information is particularly valuable for bettors looking to identify value opportunities where bookmakers may be undervaluing a team's true LAN performance potential.

## Example

Consider Team A with 70% LAN win rate but only 50% online win rate, versus Team B with 60% LAN win rate and 60% online win rate:

- Team A's weighted win rate: (0.7 * 3 + 0.5) / 4 = 0.65
- Team B's weighted win rate: (0.6 * 3 + 0.6) / 4 = 0.60

Team A has a 5% advantage in the weighted calculation, giving them an edge in our prediction model, especially for upcoming LAN events.

## Technical Implementation

The backend includes:
- Historical match tracking with LAN/online flags
- Time-weighted performance calculation
- Roster change date tracking
- Monte Carlo simulation for score prediction

The frontend displays:
- LAN/online status indicators
- Detailed performance metrics
- Visual comparison of LAN vs online win rates
- Roster stability information
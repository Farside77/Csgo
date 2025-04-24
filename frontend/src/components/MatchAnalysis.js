import React from 'react';

const MapAnalysis = ({ mapName, team1, team2, team1WinRate, team2WinRate }) => {
  const team1Percentage = Math.round(team1WinRate * 100);
  const team2Percentage = Math.round(team2WinRate * 100);
  
  return (
    <div className="map-analysis">
      <div className="map-name">{mapName}</div>
      <div className="map-stats">
        <div className="team-stat">
          <div className="team-name">{team1}</div>
          <div className="win-rate-bar">
            <div 
              className="win-rate-fill team1" 
              style={{ width: `${team1Percentage}%` }}
            ></div>
            <span className="win-rate-text">{team1Percentage}%</span>
          </div>
        </div>
        <div className="team-stat">
          <div className="team-name">{team2}</div>
          <div className="win-rate-bar">
            <div 
              className="win-rate-fill team2" 
              style={{ width: `${team2Percentage}%` }}
            ></div>
            <span className="win-rate-text">{team2Percentage}%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const MatchAnalysis = ({ match, onClose }) => {
  if (!match) return null;
  
  // Sample map data based on team names (would come from backend in production)
  const mapPool = [
    { 
      name: "Dust II", 
      team1WinRate: 0.4 + (0.5 * (match.team1.charCodeAt(0) % 10) / 10), 
      team2WinRate: 0.4 + (0.5 * (match.team2.charCodeAt(0) % 10) / 10)
    },
    { 
      name: "Mirage", 
      team1WinRate: 0.4 + (0.5 * (match.team1.charCodeAt(1) % 10) / 10), 
      team2WinRate: 0.4 + (0.5 * (match.team2.charCodeAt(1) % 10) / 10)
    },
    { 
      name: "Inferno", 
      team1WinRate: 0.4 + (0.5 * (match.team1.charCodeAt(2) % 10) / 10), 
      team2WinRate: 0.4 + (0.5 * (match.team2.charCodeAt(2) % 10) / 10)
    },
    { 
      name: "Nuke", 
      team1WinRate: 0.4 + (0.5 * (match.team1.charCodeAt(0) % 10) / 10), 
      team2WinRate: 0.4 + (0.5 * (match.team2.charCodeAt(0) % 10) / 10)
    },
    { 
      name: "Overpass", 
      team1WinRate: 0.4 + (0.5 * (match.team1.charCodeAt(1) % 10) / 10), 
      team2WinRate: 0.4 + (0.5 * (match.team2.charCodeAt(1) % 10) / 10)
    }
  ];

  // Get LAN and roster data if available
  const analysis = match.analysis || {};
  const isLan = analysis.is_lan;
  const team1LanWinRate = analysis.team1_lan_win_rate;
  const team1OnlineWinRate = analysis.team1_online_win_rate;
  const team1RosterStability = analysis.team1_roster_stability;
  const team1DaysSinceChange = analysis.team1_days_since_roster_change;
  
  const team2LanWinRate = analysis.team2_lan_win_rate;
  const team2OnlineWinRate = analysis.team2_online_win_rate;
  const team2RosterStability = analysis.team2_roster_stability;
  const team2DaysSinceChange = analysis.team2_days_since_roster_change;
  
  // Calculate average win probabilities
  const avgTeam1WinRate = mapPool.reduce((acc, map) => acc + map.team1WinRate, 0) / mapPool.length;
  const avgTeam2WinRate = mapPool.reduce((acc, map) => acc + map.team2WinRate, 0) / mapPool.length;
  
  // Normalize to sum to 1
  const total = avgTeam1WinRate + avgTeam2WinRate;
  const normalizedTeam1WinRate = avgTeam1WinRate / total;
  const normalizedTeam2WinRate = avgTeam2WinRate / total;

  return (
    <div className="modal-overlay">
      <div className="modal-content analysis-modal">
        <div className="modal-header">
          <h3>Match Analysis</h3>
          <button className="close-modal" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="match-info">
            <div className="match-teams">{match.team1} vs {match.team2}</div>
            <div className="match-event">{match.event} | {match.format}</div>
          </div>
          
          <div className="analysis-section">
            <h4>Overall Prediction</h4>
            <div className="prediction-summary">
              <div className="win-probability">
                <div className="team-probability">
                  <span className="team-name">{match.team1}</span>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill team1" 
                      style={{ width: `${normalizedTeam1WinRate * 100}%` }}
                    ></div>
                    <span className="probability-text">{Math.round(normalizedTeam1WinRate * 100)}%</span>
                  </div>
                </div>
                <div className="team-probability">
                  <span className="team-name">{match.team2}</span>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill team2" 
                      style={{ width: `${normalizedTeam2WinRate * 100}%` }}
                    ></div>
                    <span className="probability-text">{Math.round(normalizedTeam2WinRate * 100)}%</span>
                  </div>
                </div>
              </div>
              <div className="prediction-details">
                <div>Predicted Winner: <strong>{match.predicted_winner}</strong></div>
                <div>Predicted Score: <strong>{match.predicted_score}</strong></div>
                {match.ev_value && (
                  <div className={`ev-value ${match.ev_value > 0 ? 'positive' : 'negative'}`}>
                    EV: {match.ev_value > 0 ? '+' : ''}{match.ev_value.toFixed(2)}
                  </div>
                )}
              </div>
            </div>
          </div>
          
          <div className="analysis-section">
            <h4>Performance Factors</h4>
            <div className="performance-factors">
              <div className="factor-section">
                <h5>{isLan ? "🏆 LAN Event" : "🌐 Online Event"}</h5>
                <div className="team-factors">
                  <div className="team-factor">
                    <span className="team-name">{match.team1}</span>
                    <div className="factor-data">
                      {team1LanWinRate && (
                        <div className="factor-item">
                          <span className="factor-label">LAN Win Rate:</span>
                          <span className={`factor-value ${team1LanWinRate > 0.5 ? 'positive' : 'negative'}`}>
                            {(team1LanWinRate * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                      {team1OnlineWinRate && (
                        <div className="factor-item">
                          <span className="factor-label">Online Win Rate:</span>
                          <span className={`factor-value ${team1OnlineWinRate > 0.5 ? 'positive' : 'negative'}`}>
                            {(team1OnlineWinRate * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                      {team1RosterStability && (
                        <div className="factor-item">
                          <span className="factor-label">Roster Stability:</span>
                          <span className={`factor-value ${team1RosterStability > 0.5 ? 'positive' : 'negative'}`}>
                            {(team1RosterStability * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                      {team1DaysSinceChange && (
                        <div className="factor-item">
                          <span className="factor-label">Last Roster Change:</span>
                          <span className="factor-value">
                            {team1DaysSinceChange} days ago
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="team-factor">
                    <span className="team-name">{match.team2}</span>
                    <div className="factor-data">
                      {team2LanWinRate && (
                        <div className="factor-item">
                          <span className="factor-label">LAN Win Rate:</span>
                          <span className={`factor-value ${team2LanWinRate > 0.5 ? 'positive' : 'negative'}`}>
                            {(team2LanWinRate * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                      {team2OnlineWinRate && (
                        <div className="factor-item">
                          <span className="factor-label">Online Win Rate:</span>
                          <span className={`factor-value ${team2OnlineWinRate > 0.5 ? 'positive' : 'negative'}`}>
                            {(team2OnlineWinRate * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                      {team2RosterStability && (
                        <div className="factor-item">
                          <span className="factor-label">Roster Stability:</span>
                          <span className={`factor-value ${team2RosterStability > 0.5 ? 'positive' : 'negative'}`}>
                            {(team2RosterStability * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                      {team2DaysSinceChange && (
                        <div className="factor-item">
                          <span className="factor-label">Last Roster Change:</span>
                          <span className="factor-value">
                            {team2DaysSinceChange} days ago
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="analysis-section">
            <h4>Map Analysis</h4>
            <div className="map-pool">
              {mapPool.map((map, index) => (
                <MapAnalysis 
                  key={index}
                  mapName={map.name}
                  team1={match.team1}
                  team2={match.team2}
                  team1WinRate={map.team1WinRate}
                  team2WinRate={map.team2WinRate}
                />
              ))}
            </div>
          </div>
          
          <div className="analysis-section">
            <h4>Betting Recommendation</h4>
            <div className="recommendation">
              {match.ev_value > 0.1 ? (
                <div className="recommended-bet positive">
                  <div className="recommendation-header">Strong Value Bet</div>
                  <div className="recommendation-details">
                    Bet on <strong>{match.predicted_winner}</strong> with EV <strong>+{match.ev_value.toFixed(2)}</strong>
                  </div>
                  <div className="recommendation-explanation">
                    Our model predicts {match.predicted_winner} has a {Math.round(match.win_probability * 100)}% chance to win, 
                    but the odds ({match.predicted_winner === match.team1 ? match.team1_odds : match.team2_odds}) 
                    imply only a {Math.round(100 / (match.predicted_winner === match.team1 ? match.team1_odds : match.team2_odds))}% chance.
                  </div>
                </div>
              ) : match.ev_value > 0 ? (
                <div className="recommended-bet neutral">
                  <div className="recommendation-header">Slight Value</div>
                  <div className="recommendation-details">
                    Consider betting on <strong>{match.predicted_winner}</strong> with EV <strong>+{match.ev_value.toFixed(2)}</strong>
                  </div>
                </div>
              ) : (
                <div className="recommended-bet negative">
                  <div className="recommendation-header">No Value Found</div>
                  <div className="recommendation-details">
                    Odds are not favorable. Consider skipping this match.
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MatchAnalysis;
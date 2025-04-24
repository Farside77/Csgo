import { useState, useEffect } from 'react';
import "./App.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [activeTab, setActiveTab] = useState('matches');
  const [matches, setMatches] = useState([]);
  const [bets, setBets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [betForm, setBetForm] = useState({
    match_id: '',
    team_bet_on: '',
    odds: 0,
    stake: 0,
  });
  const [refreshing, setRefreshing] = useState(false);

  // Fetch matches and bets on component mount
  useEffect(() => {
    fetchMatches();
    fetchBets();
  }, []);

  const fetchMatches = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${BACKEND_URL}/matches`);
      
      if (!response.ok) {
        throw new Error(`Error fetching matches: ${response.statusText}`);
      }
      
      const data = await response.json();
      setMatches(data);
      setError(null);
    } catch (err) {
      setError(`Failed to load matches: ${err.message}`);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchBets = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/bets`);
      
      if (!response.ok) {
        throw new Error(`Error fetching bets: ${response.statusText}`);
      }
      
      const data = await response.json();
      setBets(data);
    } catch (err) {
      console.error('Failed to load bets:', err);
    }
  };

  const refreshMatches = async () => {
    try {
      setRefreshing(true);
      const response = await fetch(`${BACKEND_URL}/refresh-matches`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error(`Error refreshing matches: ${response.statusText}`);
      }
      
      await fetchMatches();
    } catch (err) {
      setError(`Failed to refresh matches: ${err.message}`);
      console.error(err);
    } finally {
      setRefreshing(false);
    }
  };

  const handleCreateBet = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/bets`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...betForm,
          odds: parseFloat(betForm.odds),
          stake: parseFloat(betForm.stake)
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Error creating bet: ${response.statusText}`);
      }
      
      // Reset form and fetch updated bets
      setBetForm({
        match_id: '',
        team_bet_on: '',
        odds: 0,
        stake: 0,
      });
      setSelectedMatch(null);
      await fetchBets();
      setActiveTab('bets');
    } catch (err) {
      console.error('Failed to create bet:', err);
    }
  };

  const handleUpdateBetResult = async (betId, result) => {
    try {
      const betToUpdate = bets.find(bet => bet.id === betId);
      
      if (!betToUpdate) return;
      
      const actual_return = result === 'win' ? betToUpdate.potential_return : 0;
      
      const response = await fetch(`${BACKEND_URL}/api/bets/${betId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          result,
          status: 'settled',
          actual_return
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Error updating bet: ${response.statusText}`);
      }
      
      await fetchBets();
    } catch (err) {
      console.error('Failed to update bet:', err);
    }
  };

  const openBetForm = (match) => {
    setSelectedMatch(match);
    setBetForm({
      match_id: match.id,
      team_bet_on: '',
      odds: 0,
      stake: 0,
    });
  };

  // Calculate betting performance metrics
  const betMetrics = bets.reduce(
    (acc, bet) => {
      if (bet.status === 'settled') {
        acc.totalBets += 1;
        acc.totalStaked += bet.stake;
        
        if (bet.result === 'win') {
          acc.wins += 1;
          acc.totalReturns += bet.actual_return;
        }
      }
      return acc;
    },
    { totalBets: 0, wins: 0, totalStaked: 0, totalReturns: 0 }
  );

  const winRate = betMetrics.totalBets > 0 ? (betMetrics.wins / betMetrics.totalBets) * 100 : 0;
  const profit = betMetrics.totalReturns - betMetrics.totalStaked;
  const roi = betMetrics.totalStaked > 0 ? (profit / betMetrics.totalStaked) * 100 : 0;

  return (
    <div className="cs2-tracker">
      <header className="app-header">
        <h1>CS2 Esports Tracker</h1>
        <p>Track matches, analyze bets, and find positive EV opportunities</p>
      </header>

      <nav className="app-nav">
        <button 
          className={`nav-button ${activeTab === 'matches' ? 'active' : ''}`}
          onClick={() => setActiveTab('matches')}
        >
          Matches
        </button>
        <button 
          className={`nav-button ${activeTab === 'bets' ? 'active' : ''}`}
          onClick={() => setActiveTab('bets')}
        >
          My Bets
        </button>
      </nav>

      <main className="app-content">
        {activeTab === 'matches' && (
          <div className="matches-container">
            <div className="content-header">
              <h2>Upcoming Matches</h2>
              <button 
                className="refresh-button"
                onClick={refreshMatches}
                disabled={refreshing}
              >
                {refreshing ? 'Refreshing...' : 'Refresh Matches'}
              </button>
            </div>
            
            {error && <div className="error-message">{error}</div>}
            
            {isLoading ? (
              <div className="loading">Loading matches...</div>
            ) : (
              <div className="matches-list">
                {matches.length === 0 ? (
                  <div className="no-data">No upcoming matches found.</div>
                ) : (
                  matches.map(match => (
                    <div key={match.id} className="match-card">
                      <div className="match-header">
                        <div className="match-event">{match.event}</div>
                        <div className="match-date">
                          {new Date(match.date).toLocaleDateString()} {new Date(match.date).toLocaleTimeString()}
                        </div>
                      </div>
                      
                      <div className="match-teams">
                        <div className={`team ${match.predicted_winner === match.team1 ? 'predicted-winner' : ''}`}>
                          {match.team1}
                          {match.team1_odds && (
                            <div className="odds-container">
                              <span className="odds">{match.team1_odds.toFixed(2)}</span>
                              {match.odds_sources && (
                                <div className="odds-tooltip">
                                  <div>HLTV: {match.odds_sources.hltv?.team1 ? match.odds_sources.hltv.team1.toFixed(2) : 'N/A'}</div>
                                  <div>GG.Bet: {match.odds_sources.ggbet?.team1 ? match.odds_sources.ggbet.team1.toFixed(2) : 'N/A'}</div>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                        <div className="vs">VS</div>
                        <div className={`team ${match.predicted_winner === match.team2 ? 'predicted-winner' : ''}`}>
                          {match.team2}
                          {match.team2_odds && (
                            <div className="odds-container">
                              <span className="odds">{match.team2_odds.toFixed(2)}</span>
                              {match.odds_sources && (
                                <div className="odds-tooltip">
                                  <div>HLTV: {match.odds_sources.hltv?.team2 ? match.odds_sources.hltv.team2.toFixed(2) : 'N/A'}</div>
                                  <div>GG.Bet: {match.odds_sources.ggbet?.team2 ? match.odds_sources.ggbet.team2.toFixed(2) : 'N/A'}</div>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                      
                      <div className="match-details">
                        <div className="match-format">{match.format}</div>
                        {match.predicted_winner && (
                          <div className="match-prediction">
                            <div>Prediction: <strong>{match.predicted_winner}</strong> ({(match.win_probability * 100).toFixed(0)}%)</div>
                            <div>Predicted Score: {match.predicted_score}</div>
                            {match.ev_value && (
                              <div className={`ev-value ${match.ev_value > 0 ? 'positive' : 'negative'}`}>
                                EV: {match.ev_value > 0 ? '+' : ''}{match.ev_value.toFixed(2)}
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                      
                      <div className="match-actions">
                        <button 
                          className="bet-button"
                          onClick={() => openBetForm(match)}
                        >
                          Place Bet
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'bets' && (
          <div className="bets-container">
            <div className="content-header">
              <h2>My Bets</h2>
              <div className="bet-metrics">
                <div className="metric">
                  <span>Total Bets:</span>
                  <strong>{betMetrics.totalBets}</strong>
                </div>
                <div className="metric">
                  <span>Win Rate:</span>
                  <strong>{winRate.toFixed(1)}%</strong>
                </div>
                <div className="metric">
                  <span>Profit:</span>
                  <strong className={profit >= 0 ? 'positive' : 'negative'}>
                    {profit >= 0 ? '+' : ''}{profit.toFixed(2)}
                  </strong>
                </div>
                <div className="metric">
                  <span>ROI:</span>
                  <strong className={roi >= 0 ? 'positive' : 'negative'}>
                    {roi >= 0 ? '+' : ''}{roi.toFixed(1)}%
                  </strong>
                </div>
              </div>
            </div>
            
            <div className="bets-list">
              {bets.length === 0 ? (
                <div className="no-data">No bets recorded yet.</div>
              ) : (
                bets.map(bet => {
                  const match = matches.find(m => m.id === bet.match_id) || { 
                    team1: 'Unknown', 
                    team2: 'Unknown' 
                  };
                  
                  return (
                    <div key={bet.id} className="bet-card">
                      <div className="bet-header">
                        <div className="bet-teams">
                          {match.team1} vs {match.team2}
                        </div>
                        <div className="bet-date">
                          {new Date(bet.created_at).toLocaleDateString()}
                        </div>
                      </div>
                      
                      <div className="bet-details">
                        <div className="bet-info">
                          <div>Bet on: <strong>{bet.team_bet_on}</strong></div>
                          <div>Odds: <strong>{bet.odds.toFixed(2)}</strong></div>
                          <div>Stake: <strong>${bet.stake.toFixed(2)}</strong></div>
                          <div>Potential Return: <strong>${bet.potential_return.toFixed(2)}</strong></div>
                        </div>
                        
                        <div className="bet-status">
                          {bet.status === 'pending' ? (
                            <div className="bet-actions">
                              <button 
                                className="win-button"
                                onClick={() => handleUpdateBetResult(bet.id, 'win')}
                              >
                                Win
                              </button>
                              <button 
                                className="loss-button"
                                onClick={() => handleUpdateBetResult(bet.id, 'loss')}
                              >
                                Loss
                              </button>
                            </div>
                          ) : (
                            <div className={`bet-result ${bet.result}`}>
                              {bet.result === 'win' ? (
                                <>
                                  <div className="result-label">Win</div>
                                  <div className="result-value">+${(bet.actual_return - bet.stake).toFixed(2)}</div>
                                </>
                              ) : (
                                <>
                                  <div className="result-label">Loss</div>
                                  <div className="result-value">-${bet.stake.toFixed(2)}</div>
                                </>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}
      </main>

      {selectedMatch && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Place Bet</h3>
              <button className="close-modal" onClick={() => setSelectedMatch(null)}>×</button>
            </div>
            
            <div className="modal-body">
              <div className="match-info">
                <div className="match-teams">{selectedMatch.team1} vs {selectedMatch.team2}</div>
                <div className="match-event">{selectedMatch.event}</div>
              </div>
              
              <form onSubmit={handleCreateBet} className="bet-form">
                <div className="form-group">
                  <label>Team to bet on</label>
                  <select
                    value={betForm.team_bet_on}
                    onChange={(e) => setBetForm({...betForm, team_bet_on: e.target.value})}
                    required
                  >
                    <option value="">Select team</option>
                    <option value={selectedMatch.team1}>{selectedMatch.team1}</option>
                    <option value={selectedMatch.team2}>{selectedMatch.team2}</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Odds</label>
                  <input
                    type="number"
                    step="0.01"
                    min="1"
                    value={betForm.odds}
                    onChange={(e) => setBetForm({...betForm, odds: e.target.value})}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Stake ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={betForm.stake}
                    onChange={(e) => setBetForm({...betForm, stake: e.target.value})}
                    required
                  />
                </div>
                
                <div className="form-group potential-return">
                  <label>Potential Return</label>
                  <div className="value">
                    ${(betForm.odds * betForm.stake).toFixed(2)}
                  </div>
                </div>
                
                <div className="form-actions">
                  <button type="submit" className="submit-bet">Place Bet</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

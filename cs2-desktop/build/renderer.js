// Renderer process - frontend logic

// Constants
const API_BASE_URL = 'http://127.0.0.1:8001/api';

// DOM Elements
const matchesList = document.getElementById('matchesList');
const betsList = document.getElementById('betsList');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');
const refreshButton = document.getElementById('refreshButton');
const restartBackendButton = document.getElementById('restartBackendButton');
const teamFilter = document.getElementById('teamFilter');
const eventFilter = document.getElementById('eventFilter');
const statusFilter = document.getElementById('statusFilter');
const lanFilter = document.getElementById('lanFilter');
const winLossRatio = document.getElementById('winLossRatio');
const profit = document.getElementById('profit');
const roi = document.getElementById('roi');

// State
let matches = [];
let bets = [];
let filters = {
    team: '',
    event: '',
    status: '',
    isLan: ''
};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the app
    fetchMatches();
    fetchBets();
    
    // Setup event listeners
    refreshButton.addEventListener('click', refreshData);
    restartBackendButton.addEventListener('click', restartBackend);
    
    // Filter event listeners
    teamFilter.addEventListener('input', updateFilters);
    eventFilter.addEventListener('input', updateFilters);
    statusFilter.addEventListener('change', updateFilters);
    lanFilter.addEventListener('change', updateFilters);
    
    // Listen for messages from the main process
    if (window.api) {
        window.api.receive('reload-data', () => {
            refreshData();
        });
    }
});

// Functions
function showLoading() {
    loadingIndicator.classList.remove('hidden');
    errorMessage.classList.add('hidden');
}

function hideLoading() {
    loadingIndicator.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function updateFilters() {
    filters.team = teamFilter.value.toLowerCase();
    filters.event = eventFilter.value.toLowerCase();
    filters.status = statusFilter.value;
    filters.isLan = lanFilter.value;
    
    renderMatches();
}

async function fetchMatches() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/matches`);
        
        if (!response.ok) {
            throw new Error(`Error fetching matches: ${response.statusText}`);
        }
        
        matches = await response.json();
        renderMatches();
    } catch (error) {
        console.error('Error fetching matches:', error);
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function fetchBets() {
    try {
        const response = await fetch(`${API_BASE_URL}/bets`);
        
        if (!response.ok) {
            throw new Error(`Error fetching bets: ${response.statusText}`);
        }
        
        bets = await response.json();
        renderBets();
        calculateStats();
    } catch (error) {
        console.error('Error fetching bets:', error);
    }
}

function refreshData() {
    fetchMatches();
    fetchBets();
}

function restartBackend() {
    if (window.api) {
        window.api.send('restart-backend');
        showLoading();
        setTimeout(() => {
            fetchMatches();
            fetchBets();
        }, 5000); // Give the backend time to restart
    }
}

function renderMatches() {
    if (!matches || matches.length === 0) {
        matchesList.innerHTML = '<p>No matches found.</p>';
        return;
    }
    
    // Filter matches
    const filteredMatches = matches.filter(match => {
        const teamMatch = filters.team ? 
            (match.team1.toLowerCase().includes(filters.team) || 
             match.team2.toLowerCase().includes(filters.team)) : true;
             
        const eventMatch = filters.event ? 
            match.event.toLowerCase().includes(filters.event) : true;
            
        const statusMatch = filters.status ? 
            match.status === filters.status : true;
            
        const lanMatch = filters.isLan ? 
            (filters.isLan === 'true' ? match.is_lan : !match.is_lan) : true;
            
        return teamMatch && eventMatch && statusMatch && lanMatch;
    });
    
    if (filteredMatches.length === 0) {
        matchesList.innerHTML = '<p>No matches found with the current filters.</p>';
        return;
    }
    
    // Sort matches by date
    filteredMatches.sort((a, b) => new Date(a.date) - new Date(b.date));
    
    // Render matches
    matchesList.innerHTML = filteredMatches.map(match => {
        const matchDate = formatDate(match.date);
        const predictedWinner = match.predicted_winner;
        const winProbability = Math.round(match.win_probability * 100);
        const evValue = match.ev_value !== null ? match.ev_value : null;
        
        let evClass = '';
        let evFormatted = '';
        
        if (evValue !== null) {
            evFormatted = (evValue * 100).toFixed(2) + '%';
            evClass = evValue > 0 ? 'ev-positive' : (evValue < 0 ? 'ev-negative' : 'ev-neutral');
        }
        
        return `
            <div class="match-card" data-id="${match.id}">
                <div class="match-header">
                    <span class="match-date">${matchDate}</span>
                    <span class="match-event">${match.event}</span>
                </div>
                
                <div class="match-teams">
                    <div class="team">
                        <span class="team-name">${match.team1}</span>
                        <span class="team-odds">${match.team1_odds ? match.team1_odds.toFixed(2) : '-'}</span>
                    </div>
                    
                    <div class="vs">VS</div>
                    
                    <div class="team">
                        <span class="team-name">${match.team2}</span>
                        <span class="team-odds">${match.team2_odds ? match.team2_odds.toFixed(2) : '-'}</span>
                    </div>
                </div>
                
                <div class="match-details">
                    <span class="match-format">${match.format || 'Unknown format'}</span>
                    <span class="match-status">${match.status}</span>
                    <span>${match.is_lan ? 'LAN' : 'Online'}</span>
                </div>
                
                <div class="match-prediction">
                    <div class="prediction-header">Prediction</div>
                    <div class="prediction-details">
                        <span class="prediction-item">Winner: ${predictedWinner}</span>
                        <span class="prediction-item">Probability: ${winProbability}%</span>
                        <span class="prediction-item">Predicted score: ${match.predicted_score || 'N/A'}</span>
                        ${evValue !== null ? `<span class="prediction-item">EV: <span class="ev-value ${evClass}">${evFormatted}</span></span>` : ''}
                    </div>
                </div>
                
                ${match.status === 'upcoming' ? `
                <div class="bet-actions">
                    <button class="btn-bet" onclick="placeBet('${match.id}', '${match.team1}', ${match.team1_odds || 0})">Bet on ${match.team1}</button>
                    <button class="btn-bet" onclick="placeBet('${match.id}', '${match.team2}', ${match.team2_odds || 0})">Bet on ${match.team2}</button>
                </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

function renderBets() {
    if (!bets || bets.length === 0) {
        betsList.innerHTML = '<p>No bets placed yet.</p>';
        return;
    }
    
    // Sort bets by date (newest first)
    bets.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    // Render bets
    betsList.innerHTML = bets.map(bet => {
        const betDate = formatDate(bet.created_at);
        let statusClass = '';
        
        switch (bet.status) {
            case 'won':
                statusClass = 'won';
                break;
            case 'lost':
                statusClass = 'lost';
                break;
            default:
                statusClass = 'pending';
        }
        
        return `
            <div class="bet-card" data-id="${bet.id}">
                <div class="bet-header">
                    <span class="bet-date">${betDate}</span>
                    <span class="bet-status ${statusClass}">${bet.status}</span>
                </div>
                
                <div class="bet-details">
                    <div class="bet-teams">${bet.team1} vs ${bet.team2}</div>
                    <div>Bet on: <strong>${bet.bet_on}</strong></div>
                    
                    <div class="bet-info">
                        <span class="bet-item">Amount: $${bet.amount.toFixed(2)}</span>
                        <span class="bet-item">Odds: ${bet.odds.toFixed(2)}</span>
                        ${bet.status === 'won' ? `<span class="bet-item">Profit: $${(bet.amount * bet.odds - bet.amount).toFixed(2)}</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function calculateStats() {
    if (!bets || bets.length === 0) {
        winLossRatio.textContent = 'N/A';
        profit.textContent = '$0.00';
        roi.textContent = '0.00%';
        return;
    }
    
    const wins = bets.filter(bet => bet.status === 'won').length;
    const losses = bets.filter(bet => bet.status === 'lost').length;
    const ratio = losses > 0 ? (wins / losses).toFixed(2) : wins > 0 ? '∞' : '0.00';
    
    let totalProfit = 0;
    let totalInvestment = 0;
    
    bets.forEach(bet => {
        if (bet.status === 'won') {
            totalProfit += bet.amount * bet.odds - bet.amount;
        } else if (bet.status === 'lost') {
            totalProfit -= bet.amount;
        }
        
        if (bet.status === 'won' || bet.status === 'lost') {
            totalInvestment += bet.amount;
        }
    });
    
    const roiValue = totalInvestment > 0 ? (totalProfit / totalInvestment * 100).toFixed(2) : '0.00';
    
    winLossRatio.textContent = `${wins}W - ${losses}L (${ratio})`;
    profit.textContent = `$${totalProfit.toFixed(2)}`;
    profit.style.color = totalProfit >= 0 ? '#065f46' : '#b91c1c';
    roi.textContent = `${roiValue}%`;
    roi.style.color = parseFloat(roiValue) >= 0 ? '#065f46' : '#b91c1c';
}

// Function to place a bet
window.placeBet = async function(matchId, teamName, odds) {
    if (!odds) {
        alert('No odds available for this bet.');
        return;
    }
    
    const amount = parseFloat(prompt(`How much do you want to bet on ${teamName}?`, '10'));
    
    if (isNaN(amount) || amount <= 0) {
        alert('Please enter a valid amount.');
        return;
    }
    
    const match = matches.find(m => m.id === matchId);
    
    if (!match) {
        alert('Match not found.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/bets`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                match_id: matchId,
                bet_on: teamName,
                team1: match.team1,
                team2: match.team2,
                odds: odds,
                amount: amount,
                status: 'pending'
            }),
        });
        
        if (!response.ok) {
            throw new Error(`Error placing bet: ${response.statusText}`);
        }
        
        const newBet = await response.json();
        bets.push(newBet);
        renderBets();
        calculateStats();
        
        alert(`Bet placed successfully on ${teamName}.`);
    } catch (error) {
        console.error('Error placing bet:', error);
        alert(`Failed to place bet: ${error.message}`);
    }
};
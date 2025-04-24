import React, { useState, useEffect } from 'react';

const MatchFilter = ({ matches, onFilter }) => {
  const [filters, setFilters] = useState({
    team: '',
    event: '',
    format: '',
    dateRange: 7, // days
    evFilter: 'all' // all, positive, negative
  });
  
  const [events, setEvents] = useState([]);
  const [teams, setTeams] = useState([]);
  const [formats, setFormats] = useState([]);
  
  // Extract unique values for filter dropdowns
  useEffect(() => {
    if (!matches || !matches.length) return;
    
    const allEvents = [...new Set(matches.map(match => match.event))];
    const allTeams = [...new Set([
      ...matches.map(match => match.team1),
      ...matches.map(match => match.team2)
    ])];
    const allFormats = [...new Set(matches.map(match => match.format))];
    
    setEvents(allEvents);
    setTeams(allTeams);
    setFormats(allFormats);
  }, [matches]);
  
  // Apply filters when they change
  useEffect(() => {
    if (!matches) return;
    
    const filteredMatches = matches.filter(match => {
      // Team filter
      if (filters.team && match.team1 !== filters.team && match.team2 !== filters.team) {
        return false;
      }
      
      // Event filter
      if (filters.event && match.event !== filters.event) {
        return false;
      }
      
      // Format filter
      if (filters.format && match.format !== filters.format) {
        return false;
      }
      
      // Date range filter
      if (filters.dateRange > 0) {
        const matchDate = new Date(match.date);
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - filters.dateRange);
        if (matchDate < cutoffDate) {
          return false;
        }
      }
      
      // EV filter
      if (filters.evFilter !== 'all' && match.ev_value !== undefined) {
        if (filters.evFilter === 'positive' && match.ev_value <= 0) {
          return false;
        }
        if (filters.evFilter === 'negative' && match.ev_value >= 0) {
          return false;
        }
      }
      
      return true;
    });
    
    onFilter(filteredMatches);
  }, [filters, matches, onFilter]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };
  
  const handleEvFilterChange = (value) => {
    setFilters(prev => ({ ...prev, evFilter: value }));
  };
  
  const resetFilters = () => {
    setFilters({
      team: '',
      event: '',
      format: '',
      dateRange: 7,
      evFilter: 'all'
    });
  };
  
  return (
    <div className="filter-controls">
      <div className="filter-form">
        <div className="filter-group">
          <label className="filter-label">Team</label>
          <select 
            name="team"
            value={filters.team}
            onChange={handleChange}
            className="filter-select"
          >
            <option value="">All Teams</option>
            {teams.map((team, index) => (
              <option key={index} value={team}>{team}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Event</label>
          <select 
            name="event"
            value={filters.event}
            onChange={handleChange}
            className="filter-select"
          >
            <option value="">All Events</option>
            {events.map((event, index) => (
              <option key={index} value={event}>{event}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Format</label>
          <select 
            name="format"
            value={filters.format}
            onChange={handleChange}
            className="filter-select"
          >
            <option value="">All Formats</option>
            {formats.map((format, index) => (
              <option key={index} value={format}>{format}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Time Range</label>
          <select 
            name="dateRange"
            value={filters.dateRange}
            onChange={handleChange}
            className="filter-select"
          >
            <option value={1}>Next 24 hours</option>
            <option value={3}>Next 3 days</option>
            <option value={7}>Next week</option>
            <option value={14}>Next 2 weeks</option>
            <option value={30}>Next month</option>
            <option value={0}>All matches</option>
          </select>
        </div>
      </div>
      
      <div className="filter-options">
        <span className="filter-label">EV Filter:</span>
        <button 
          className={`filter-option ${filters.evFilter === 'all' ? 'active' : ''}`} 
          onClick={() => handleEvFilterChange('all')}
        >
          All
        </button>
        <button 
          className={`filter-option ${filters.evFilter === 'positive' ? 'active' : ''}`} 
          onClick={() => handleEvFilterChange('positive')}
        >
          Positive EV
        </button>
        <button 
          className={`filter-option ${filters.evFilter === 'negative' ? 'active' : ''}`} 
          onClick={() => handleEvFilterChange('negative')}
        >
          Negative EV
        </button>
        
        <button className="filter-reset" onClick={resetFilters}>
          Reset Filters
        </button>
      </div>
    </div>
  );
};

export default MatchFilter;
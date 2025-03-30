import { useState, useEffect } from 'react';
import './PropertyScraper.css';
import { Button, Input } from './ui';
import scraperApi, { ScraperParams, TaskStatus } from '../api/scraperApi';

const propertyTypeOptions = [
  { value: 'casas', label: 'Casas' },
  { value: 'apartamentos', label: 'Apartamentos' },
  { value: 'fincas', label: 'Fincas' },
  { value: 'casas-campestres', label: 'Casas Campestres' },
  { value: 'cabanas', label: 'Cabañas' }
];

const PropertyScraper = () => {
  const [formData, setFormData] = useState<ScraperParams>({
    city: '',
    region: '',
    property_types: ['casas'],
    max_pages: 5,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [logs, setLogs] = useState<string[]>([]);
  const [recentTasks, setRecentTasks] = useState<TaskStatus[]>([]);
  const [isLoadingLogs, setIsLoadingLogs] = useState(false);
  const [isLoadingTasks, setIsLoadingTasks] = useState(false);
  const [activeTab, setActiveTab] = useState<'form' | 'tasks' | 'logs'>('form');

  // Load recent tasks and logs on mount
  useEffect(() => {
    fetchRecentTasks();
    fetchRecentLogs();
  }, []);

  // Refresh logs every 5 seconds if on logs tab
  useEffect(() => {
    let interval: number | undefined;
    
    if (activeTab === 'logs') {
      interval = window.setInterval(() => {
        fetchRecentLogs();
      }, 5000);
    }
    
    return () => {
      if (interval) window.clearInterval(interval);
    };
  }, [activeTab]);

  // Refresh tasks every 5 seconds if on tasks tab
  useEffect(() => {
    let interval: number | undefined;
    
    if (activeTab === 'tasks') {
      interval = window.setInterval(() => {
        fetchRecentTasks();
      }, 5000);
    }
    
    return () => {
      if (interval) window.clearInterval(interval);
    };
  }, [activeTab]);

  const fetchRecentLogs = async () => {
    try {
      setIsLoadingLogs(true);
      const response = await scraperApi.getScraperLogs();
      setLogs(response.logs);
    } catch (err) {
      console.error('Error fetching logs:', err);
    } finally {
      setIsLoadingLogs(false);
    }
  };

  const fetchRecentTasks = async () => {
    try {
      setIsLoadingTasks(true);
      const response = await scraperApi.getScraperStatus();
      setRecentTasks(response.tasks);
    } catch (err) {
      console.error('Error fetching tasks:', err);
    } finally {
      setIsLoadingTasks(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    setFormData({
      ...formData,
      [name]: type === 'number' ? Number(value) : value,
    });
  };

  const handlePropertyTypeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value, checked } = e.target;
    
    if (checked) {
      setFormData({
        ...formData,
        property_types: [...formData.property_types, value]
      });
    } else {
      setFormData({
        ...formData,
        property_types: formData.property_types.filter(type => type !== value)
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await scraperApi.startScraper(formData);
      setMessage(response.message);
      
      // Switch to Tasks tab and refresh tasks
      setActiveTab('tasks');
      fetchRecentTasks();
    } catch (err) {
      setError('Failed to start scraper. Please try again.');
      console.error('Scraping error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const renderTabs = () => {
    return (
      <div className="tabs">
        <button 
          className={`tab-button ${activeTab === 'form' ? 'active' : ''}`}
          onClick={() => setActiveTab('form')}
        >
          Start Scraper
        </button>
        <button 
          className={`tab-button ${activeTab === 'tasks' ? 'active' : ''}`}
          onClick={() => { setActiveTab('tasks'); fetchRecentTasks(); }}
        >
          Recent Tasks
        </button>
        <button 
          className={`tab-button ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => { setActiveTab('logs'); fetchRecentLogs(); }}
        >
          Logs
        </button>
      </div>
    );
  };

  const renderTasksList = () => {
    if (isLoadingTasks) {
      return <div className="loading-indicator">Loading tasks...</div>;
    }

    if (recentTasks.length === 0) {
      return <div className="no-data">No tasks found</div>;
    }

    return (
      <div className="tasks-list">
        {recentTasks.map(task => (
          <div key={task.id} className={`task-item ${task.status}`}>
            <div className="task-header">
              <span className="task-id">ID: {task.id}</span>
              <span className={`task-status ${task.status}`}>{task.status}</span>
            </div>
            <div className="task-details">
              <p><strong>Location:</strong> {task.city}, {task.region}</p>
              <p><strong>Property Type:</strong> {task.property_type}</p>
              <p><strong>Started:</strong> {new Date(task.start_time).toLocaleString()}</p>
              {task.end_time && (
                <p><strong>Ended:</strong> {new Date(task.end_time).toLocaleString()}</p>
              )}
              {task.properties_found !== undefined && (
                <p><strong>Properties Found:</strong> {task.properties_found}</p>
              )}
              {task.duration_seconds !== undefined && (
                <p><strong>Duration:</strong> {task.duration_seconds} seconds</p>
              )}
              {task.error && (
                <p className="error"><strong>Error:</strong> {task.error}</p>
              )}
            </div>
          </div>
        ))}
        <Button onClick={fetchRecentTasks} className="refresh-button">
          Refresh Tasks
        </Button>
      </div>
    );
  };

  const renderLogs = () => {
    if (isLoadingLogs) {
      return <div className="loading-indicator">Loading logs...</div>;
    }

    if (logs.length === 0) {
      return <div className="no-data">No logs found</div>;
    }

    return (
      <div className="logs-container">
        <div className="logs-list">
          {logs.map((log, index) => (
            <div key={index} className={`log-entry ${log.includes('ERROR') ? 'error' : ''}`}>
              {log}
            </div>
          ))}
        </div>
        <Button onClick={fetchRecentLogs} className="refresh-button">
          Refresh Logs
        </Button>
      </div>
    );
  };

  const renderForm = () => {
    return (
      <form onSubmit={handleSubmit} className="scraper-form">
        <div className="form-group">
          <label htmlFor="city" className="form-label">City</label>
          <Input
            type="text"
            id="city"
            name="city"
            value={formData.city}
            onChange={handleChange}
            placeholder="e.g., manizales"
            fullWidth
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="region" className="form-label">Region</label>
          <Input
            type="text"
            id="region"
            name="region"
            value={formData.region}
            onChange={handleChange}
            placeholder="e.g., caldas"
            fullWidth
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Property Types</label>
          <div className="checkbox-container">
            {propertyTypeOptions.map(option => (
              <div key={option.value} className="checkbox-wrapper">
                <input
                  type="checkbox"
                  id={`type-${option.value}`}
                  name="propertyTypes"
                  value={option.value}
                  checked={formData.property_types.includes(option.value)}
                  onChange={handlePropertyTypeChange}
                  className="checkbox-input"
                />
                <label htmlFor={`type-${option.value}`} className="checkbox-label">{option.label}</label>
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="max_pages" className="form-label">Max Pages to Scrape</label>
          <Input
            type="number"
            id="max_pages"
            name="max_pages"
            value={formData.max_pages.toString()}
            onChange={handleChange}
            min={1}
            max={50}
            fullWidth
            helpText="(1-50 pages)"
          />
        </div>

        <Button 
          type="submit" 
          isLoading={isLoading}
          disabled={isLoading || formData.property_types.length === 0}
          className="scrape-button"
          fullWidth
        >
          {isLoading ? 'Starting Scraper...' : 'Start Scraping'}
        </Button>

        {message && (
          <div className="message-container success">
            <p>{message}</p>
          </div>
        )}

        {error && (
          <div className="message-container error">
            <p>{error}</p>
          </div>
        )}
      </form>
    );
  };

  return (
    <div className="scraper-container">
      <div className="scraper-header">
        <h2>Property Scraper</h2>
        <p>Collect property listings from FincaRaiz and track scraping tasks</p>
      </div>

      {renderTabs()}

      <div className="tab-content">
        {activeTab === 'form' && renderForm()}
        {activeTab === 'tasks' && renderTasksList()}
        {activeTab === 'logs' && renderLogs()}
      </div>

      {activeTab === 'form' && (
        <div className="scraper-info">
          <h3>How it works</h3>
          <p>
            The scraper will collect property listings from FincaRaiz for the specified city, region, and property types.
            The data will be saved to the database and will be available through the API.
          </p>
          <p>
            <strong>Note:</strong> The scraping process runs in the background and may take some time 
            depending on the number of pages and selected property types.
          </p>
        </div>
      )}
    </div>
  );
};

export default PropertyScraper; 
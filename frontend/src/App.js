import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Main App Component
function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [contacts, setContacts] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  // Load initial data
  useEffect(() => {
    loadContacts();
    loadCampaigns();
    loadAnalytics();
  }, []);

  const loadContacts = async () => {
    try {
      const response = await axios.get(`${API}/contacts`);
      setContacts(response.data);
    } catch (error) {
      console.error('Error loading contacts:', error);
    }
  };

  const loadCampaigns = async () => {
    try {
      const response = await axios.get(`${API}/campaigns`);
      setCampaigns(response.data);
    } catch (error) {
      console.error('Error loading campaigns:', error);
    }
  };

  const loadAnalytics = async () => {
    try {
      const response = await axios.get(`${API}/analytics`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error loading analytics:', error);
    }
  };

  return (
    <div className="app">
      <Sidebar currentView={currentView} setCurrentView={setCurrentView} />
      <main className="main-content">
        {currentView === 'dashboard' && (
          <Dashboard 
            analytics={analytics} 
            contacts={contacts}
            campaigns={campaigns}
          />
        )}
        {currentView === 'contacts' && (
          <ContactsView 
            contacts={contacts} 
            loadContacts={loadContacts}
          />
        )}
        {currentView === 'discovery' && <DiscoveryView />}
        {currentView === 'campaigns' && (
          <CampaignsView 
            campaigns={campaigns}
            loadCampaigns={loadCampaigns}
            contacts={contacts}
          />
        )}
        {currentView === 'email-generator' && (
          <EmailGeneratorView contacts={contacts} />
        )}
        {currentView === 'analytics' && (
          <AnalyticsView analytics={analytics} />
        )}
      </main>
    </div>
  );
}

// Sidebar Component
const Sidebar = ({ currentView, setCurrentView }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'contacts', label: 'Contacts', icon: '👥' },
    { id: 'discovery', label: 'Contact Discovery', icon: '🔍' },
    { id: 'email-generator', label: 'AI Email Generator', icon: '✉️' },
    { id: 'campaigns', label: 'Campaigns', icon: '📢' },
    { id: 'analytics', label: 'Analytics', icon: '📈' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">NetworkingAI</h1>
        <p className="sidebar-subtitle">Intelligent Networking Assistant</p>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <button
            key={item.id}
            className={`nav-item ${currentView === item.id ? 'active' : ''}`}
            onClick={() => setCurrentView(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
};

// Dashboard Component
const Dashboard = ({ analytics, contacts, campaigns }) => {
  const recentContacts = contacts.slice(0, 5);
  const activeCampaigns = campaigns.filter(c => c.status === 'active').slice(0, 3);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="hero-section">
          <img 
            src="https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHxBSSUyMHRlY2hub2xvZ3l8ZW58MHx8fHwxNzU0MDk3NDExfDA&ixlib=rb-4.1.0&q=85"
            alt="NetworkingAI Hero"
            className="hero-image"
          />
          <div className="hero-content">
            <h1 className="hero-title">Welcome to NetworkingAI</h1>
            <p className="hero-description">Your intelligent networking assistant for building meaningful professional relationships</p>
          </div>
        </div>
      </header>

      <div className="dashboard-grid">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">👥</div>
            <div className="stat-content">
              <h3 className="stat-number">{analytics?.total_contacts || 0}</h3>
              <p className="stat-label">Total Contacts</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📢</div>
            <div className="stat-content">
              <h3 className="stat-number">{analytics?.total_campaigns || 0}</h3>
              <p className="stat-label">Active Campaigns</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <h3 className="stat-number">{analytics?.email_performance?.response_rate?.toFixed(1) || 0}%</h3>
              <p className="stat-label">Response Rate</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⭐</div>
            <div className="stat-content">
              <h3 className="stat-number">{analytics?.relationship_scores?.average_lead_score?.toFixed(0) || 0}</h3>
              <p className="stat-label">Avg Lead Score</p>
            </div>
          </div>
        </div>

        <div className="dashboard-sections">
          <div className="dashboard-section">
            <h2 className="section-title">Recent Contacts</h2>
            <div className="contact-list">
              {recentContacts.length > 0 ? recentContacts.map(contact => (
                <div key={contact.id} className="contact-item">
                  <div className="contact-avatar">{contact.name.charAt(0)}</div>
                  <div className="contact-info">
                    <h4 className="contact-name">{contact.name}</h4>
                    <p className="contact-company">{contact.company} • {contact.position}</p>
                  </div>
                  <div className="contact-score">{contact.lead_score}</div>
                </div>
              )) : (
                <p className="empty-state">No contacts yet. Start by adding some contacts!</p>
              )}
            </div>
          </div>

          <div className="dashboard-section">
            <h2 className="section-title">Active Campaigns</h2>
            <div className="campaign-list">
              {activeCampaigns.length > 0 ? activeCampaigns.map(campaign => (
                <div key={campaign.id} className="campaign-item">
                  <div className="campaign-info">
                    <h4 className="campaign-name">{campaign.name}</h4>
                    <p className="campaign-stats">{campaign.contact_ids.length} contacts • {campaign.sent_count} sent</p>
                  </div>
                  <div className="campaign-status active">Active</div>
                </div>
              )) : (
                <p className="empty-state">No active campaigns. Create your first campaign!</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Contacts View Component
const ContactsView = ({ contacts, loadContacts }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '', email: '', company: '', position: '', industry: '', 
    linkedin_url: '', phone: '', notes: '', priority: 'medium', tags: []
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/contacts`, formData);
      setShowForm(false);
      setFormData({
        name: '', email: '', company: '', position: '', industry: '', 
        linkedin_url: '', phone: '', notes: '', priority: 'medium', tags: []
      });
      loadContacts();
    } catch (error) {
      console.error('Error creating contact:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="contacts-view">
      <div className="view-header">
        <h1 className="view-title">Contacts</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(true)}
        >
          Add Contact
        </button>
      </div>

      {showForm && (
        <div className="modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Add New Contact</h2>
              <button className="modal-close" onClick={() => setShowForm(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit} className="contact-form">
              <div className="form-grid">
                <input
                  type="text"
                  name="name"
                  placeholder="Full Name *"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  className="form-input"
                />
                <input
                  type="email"
                  name="email"
                  placeholder="Email Address *"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  className="form-input"
                />
                <input
                  type="text"
                  name="company"
                  placeholder="Company"
                  value={formData.company}
                  onChange={handleInputChange}
                  className="form-input"
                />
                <input
                  type="text"
                  name="position"
                  placeholder="Position"
                  value={formData.position}
                  onChange={handleInputChange}
                  className="form-input"
                />
                <input
                  type="text"
                  name="industry"
                  placeholder="Industry"
                  value={formData.industry}
                  onChange={handleInputChange}
                  className="form-input"
                />
                <input
                  type="url"
                  name="linkedin_url"
                  placeholder="LinkedIn URL"
                  value={formData.linkedin_url}
                  onChange={handleInputChange}
                  className="form-input"
                />
                <input
                  type="tel"
                  name="phone"
                  placeholder="Phone Number"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="form-input"
                />
                <select
                  name="priority"
                  value={formData.priority}
                  onChange={handleInputChange}
                  className="form-input"
                >
                  <option value="low">Low Priority</option>
                  <option value="medium">Medium Priority</option>
                  <option value="high">High Priority</option>
                </select>
              </div>
              <textarea
                name="notes"
                placeholder="Notes"
                value={formData.notes}
                onChange={handleInputChange}
                className="form-textarea"
                rows="3"
              />
              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Add Contact
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="contacts-grid">
        {contacts.map(contact => (
          <div key={contact.id} className="contact-card">
            <div className="contact-card-header">
              <div className="contact-avatar">{contact.name.charAt(0)}</div>
              <div className="contact-info">
                <h3 className="contact-name">{contact.name}</h3>
                <p className="contact-company">{contact.company}</p>
                <p className="contact-position">{contact.position}</p>
              </div>
              <div className="contact-score">{contact.lead_score}</div>
            </div>
            <div className="contact-card-body">
              <p className="contact-email">{contact.email}</p>
              {contact.industry && <span className="contact-tag">{contact.industry}</span>}
              <span className={`contact-priority ${contact.priority}`}>{contact.priority} priority</span>
            </div>
            <div className="contact-card-footer">
              <span className={`contact-status ${contact.status}`}>{contact.status}</span>
              {contact.last_contacted && (
                <span className="contact-last-contact">
                  Last contacted: {new Date(contact.last_contacted).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {contacts.length === 0 && (
        <div className="empty-state">
          <h3>No contacts yet</h3>
          <p>Start building your network by adding your first contact</p>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>
            Add Your First Contact
          </button>
        </div>
      )}
    </div>
  );
};

// Discovery View Component
const DiscoveryView = () => {
  const [criteria, setCriteria] = useState({
    industry: '', role: '', company_size: '', location: ''
  });
  const [discoveredContacts, setDiscoveredContacts] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API}/discover-contacts`, criteria);
      setDiscoveredContacts(response.data.discovered_contacts);
    } catch (error) {
      console.error('Error discovering contacts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCriteria(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="discovery-view">
      <div className="view-header">
        <h1 className="view-title">Contact Discovery</h1>
        <p className="view-description">Find potential networking contacts based on your criteria</p>
      </div>

      <div className="discovery-form-card">
        <h2>Search Criteria</h2>
        <form onSubmit={handleSearch} className="discovery-form">
          <div className="form-grid">
            <input
              type="text"
              name="industry"
              placeholder="Industry (e.g., Technology)"
              value={criteria.industry}
              onChange={handleInputChange}
              className="form-input"
            />
            <input
              type="text"
              name="role"
              placeholder="Role (e.g., Software Engineer)"
              value={criteria.role}
              onChange={handleInputChange}
              className="form-input"
            />
            <select
              name="company_size"
              value={criteria.company_size}
              onChange={handleInputChange}
              className="form-input"
            >
              <option value="">Company Size</option>
              <option value="startup">Startup (1-50)</option>
              <option value="small">Small (51-200)</option>
              <option value="medium">Medium (201-1000)</option>
              <option value="large">Large (1000+)</option>
            </select>
            <input
              type="text"
              name="location"
              placeholder="Location"
              value={criteria.location}
              onChange={handleInputChange}
              className="form-input"
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Searching...' : 'Discover Contacts'}
          </button>
        </form>
      </div>

      {discoveredContacts.length > 0 && (
        <div className="discovered-contacts">
          <h2>Discovered Contacts</h2>
          <div className="contacts-grid">
            {discoveredContacts.map((contact, index) => (
              <div key={index} className="contact-card">
                <div className="contact-card-header">
                  <div className="contact-avatar">{contact.name.charAt(0)}</div>
                  <div className="contact-info">
                    <h3 className="contact-name">{contact.name}</h3>
                    <p className="contact-company">{contact.company}</p>
                    <p className="contact-position">{contact.position}</p>
                  </div>
                  <div className="contact-score">{contact.lead_score}</div>
                </div>
                <div className="contact-card-body">
                  <p className="contact-email">{contact.email}</p>
                  <span className="contact-tag">{contact.industry}</span>
                </div>
                <div className="contact-card-footer">
                  <button className="btn btn-sm btn-primary">Add to Contacts</button>
                  <a href={contact.linkedin_url} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-secondary">
                    View LinkedIn
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Email Generator View Component
const EmailGeneratorView = ({ contacts }) => {
  const [selectedContact, setSelectedContact] = useState('');
  const [emailType, setEmailType] = useState('introduction');
  const [tone, setTone] = useState('professional');
  const [context, setContext] = useState('');
  const [generatedEmail, setGeneratedEmail] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!selectedContact) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API}/generate-email`, {
        contact_id: selectedContact,
        email_type: emailType,
        context: context,
        tone: tone
      });
      setGeneratedEmail(response.data);
    } catch (error) {
      console.error('Error generating email:', error);
      setGeneratedEmail({
        subject: 'Error generating email',
        body: 'Please make sure your OpenAI API key is configured in the backend .env file.',
        personalization_notes: ['API key configuration required']
      });
    } finally {
      setLoading(false);
    }
  };

  const selectedContactData = contacts.find(c => c.id === selectedContact);

  return (
    <div className="email-generator-view">
      <div className="view-header">
        <h1 className="view-title">AI Email Generator</h1>
        <p className="view-description">Generate personalized networking emails with AI</p>
      </div>

      <div className="email-generator-grid">
        <div className="generator-form-card">
          <h2>Email Configuration</h2>
          <form onSubmit={handleGenerate} className="generator-form">
            <div className="form-group">
              <label className="form-label">Select Contact</label>
              <select
                value={selectedContact}
                onChange={(e) => setSelectedContact(e.target.value)}
                className="form-input"
                required
              >
                <option value="">Choose a contact...</option>
                {contacts.map(contact => (
                  <option key={contact.id} value={contact.id}>
                    {contact.name} - {contact.company}
                  </option>
                ))}
              </select>
            </div>

            {selectedContactData && (
              <div className="contact-preview">
                <h3>Contact Info</h3>
                <p><strong>Name:</strong> {selectedContactData.name}</p>
                <p><strong>Company:</strong> {selectedContactData.company}</p>
                <p><strong>Position:</strong> {selectedContactData.position}</p>
                <p><strong>Industry:</strong> {selectedContactData.industry}</p>
              </div>
            )}

            <div className="form-group">
              <label className="form-label">Email Type</label>
              <select
                value={emailType}
                onChange={(e) => setEmailType(e.target.value)}
                className="form-input"
              >
                <option value="introduction">Introduction</option>
                <option value="follow_up">Follow Up</option>
                <option value="meeting_request">Meeting Request</option>
                <option value="thank_you">Thank You</option>
                <option value="reconnection">Reconnection</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Tone</label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="form-input"
              >
                <option value="professional">Professional</option>
                <option value="friendly">Friendly</option>
                <option value="casual">Casual</option>
                <option value="formal">Formal</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Additional Context</label>
              <textarea
                value={context}
                onChange={(e) => setContext(e.target.value)}
                placeholder="Any additional context or specific points to include..."
                className="form-textarea"
                rows="4"
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading || !selectedContact}>
              {loading ? 'Generating...' : 'Generate Email'}
            </button>
          </form>
        </div>

        {generatedEmail && (
          <div className="generated-email-card">
            <h2>Generated Email</h2>
            <div className="email-preview">
              <div className="email-field">
                <label className="email-label">Subject:</label>
                <div className="email-content">{generatedEmail.subject}</div>
              </div>
              <div className="email-field">
                <label className="email-label">Body:</label>
                <div className="email-content email-body">{generatedEmail.body}</div>
              </div>
              {generatedEmail.personalization_notes && generatedEmail.personalization_notes.length > 0 && (
                <div className="email-field">
                  <label className="email-label">Personalization Notes:</label>
                  <ul className="personalization-notes">
                    {generatedEmail.personalization_notes.map((note, index) => (
                      <li key={index}>{note}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            <div className="email-actions">
              <button className="btn btn-secondary" onClick={() => navigator.clipboard.writeText(`Subject: ${generatedEmail.subject}\n\n${generatedEmail.body}`)}>
                Copy to Clipboard
              </button>
              <button className="btn btn-primary">Send Email</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Campaigns View Component
const CampaignsView = ({ campaigns, loadCampaigns, contacts }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '', description: '', contact_ids: [], template_id: '', scheduled_at: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/campaigns`, formData);
      setShowForm(false);
      setFormData({
        name: '', description: '', contact_ids: [], template_id: '', scheduled_at: ''
      });
      loadCampaigns();
    } catch (error) {
      console.error('Error creating campaign:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="campaigns-view">
      <div className="view-header">
        <h1 className="view-title">Email Campaigns</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(true)}
        >
          Create Campaign
        </button>
      </div>

      {showForm && (
        <div className="modal">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Create New Campaign</h2>
              <button className="modal-close" onClick={() => setShowForm(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit} className="campaign-form">
              <input
                type="text"
                name="name"
                placeholder="Campaign Name *"
                value={formData.name}
                onChange={handleInputChange}
                required
                className="form-input"
              />
              <textarea
                name="description"
                placeholder="Campaign Description"
                value={formData.description}
                onChange={handleInputChange}
                className="form-textarea"
                rows="3"
              />
              <input
                type="datetime-local"
                name="scheduled_at"
                value={formData.scheduled_at}
                onChange={handleInputChange}
                className="form-input"
              />
              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Campaign
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="campaigns-grid">
        {campaigns.map(campaign => (
          <div key={campaign.id} className="campaign-card">
            <div className="campaign-header">
              <h3 className="campaign-name">{campaign.name}</h3>
              <span className={`campaign-status ${campaign.status}`}>{campaign.status}</span>
            </div>
            <div className="campaign-body">
              <p className="campaign-description">{campaign.description}</p>
              <div className="campaign-stats">
                <div className="stat">
                  <span className="stat-label">Contacts:</span>
                  <span className="stat-value">{campaign.contact_ids.length}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Sent:</span>
                  <span className="stat-value">{campaign.sent_count}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Responses:</span>
                  <span className="stat-value">{campaign.response_count}</span>
                </div>
              </div>
            </div>
            <div className="campaign-footer">
              <span className="campaign-date">
                Created: {new Date(campaign.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        ))}
      </div>
      
      {campaigns.length === 0 && (
        <div className="empty-state">
          <h3>No campaigns yet</h3>
          <p>Create your first campaign to start networking at scale</p>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>
            Create Your First Campaign
          </button>
        </div>
      )}
    </div>
  );
};

// Analytics View Component
const AnalyticsView = ({ analytics }) => {
  if (!analytics) {
    return (
      <div className="analytics-view">
        <div className="view-header">
          <h1 className="view-title">Analytics</h1>
        </div>
        <div className="loading">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="analytics-view">
      <div className="view-header">
        <h1 className="view-title">Analytics & Insights</h1>
        <p className="view-description">Track your networking performance and ROI</p>
      </div>

      <div className="analytics-grid">
        <div className="analytics-section">
          <h2 className="section-title">Contact Overview</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3 className="stat-number">{analytics.total_contacts}</h3>
              <p className="stat-label">Total Contacts</p>
            </div>
            <div className="stat-card">
              <h3 className="stat-number">{analytics.monthly_growth.new_contacts}</h3>
              <p className="stat-label">New This Month</p>
            </div>
            <div className="stat-card">
              <h3 className="stat-number">{analytics.relationship_scores.average_lead_score.toFixed(0)}</h3>
              <p className="stat-label">Avg Lead Score</p>
            </div>
            <div className="stat-card">
              <h3 className="stat-number">{analytics.relationship_scores.average_relationship_strength.toFixed(0)}</h3>
              <p className="stat-label">Avg Relationship Strength</p>
            </div>
          </div>
        </div>

        <div className="analytics-section">
          <h2 className="section-title">Email Performance</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3 className="stat-number">{analytics.email_performance.total_sent}</h3>
              <p className="stat-label">Emails Sent</p>
            </div>
            <div className="stat-card">
              <h3 className="stat-number">{analytics.email_performance.total_responses}</h3>
              <p className="stat-label">Responses</p>
            </div>
            <div className="stat-card">
              <h3 className="stat-number">{analytics.email_performance.response_rate.toFixed(1)}%</h3>
              <p className="stat-label">Response Rate</p>
            </div>
            <div className="stat-card">
              <h3 className="stat-number">{analytics.email_performance.conversion_rate.toFixed(1)}%</h3>
              <p className="stat-label">Conversion Rate</p>
            </div>
          </div>
        </div>

        <div className="analytics-section">
          <h2 className="section-title">Contact Distribution</h2>
          <div className="distribution-grid">
            <div className="distribution-card">
              <h3>By Status</h3>
              <div className="distribution-list">
                {Object.entries(analytics.contacts_by_status).map(([status, count]) => (
                  <div key={status} className="distribution-item">
                    <span className="distribution-label">{status}</span>
                    <span className="distribution-value">{count}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="distribution-card">
              <h3>By Priority</h3>
              <div className="distribution-list">
                {Object.entries(analytics.contacts_by_priority).map(([priority, count]) => (
                  <div key={priority} className="distribution-item">
                    <span className="distribution-label">{priority}</span>
                    <span className="distribution-value">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
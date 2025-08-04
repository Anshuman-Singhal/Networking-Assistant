# 🚀 NetworkingAI - Complete User Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [User Guide](#user-guide)
6. [Troubleshooting](#troubleshooting)
7. [API Documentation](#api-documentation)
8. [Deployment Guide](#deployment-guide)

---

## 🚀 Quick Start

### For Complete Beginners (Never Used This Project Before)

**Step 1: Fix Any Issues**
```bash
# Run the fix script to ensure everything works
chmod +x /app/fix-services.sh
/app/fix-services.sh
```

**Step 2: Configure OpenAI (Optional but Recommended)**
```bash
# Edit the backend environment file
nano /app/backend/.env

# Replace YOUR_OPENAI_API_KEY_HERE with your actual OpenAI API key
# Get your key from: https://platform.openai.com/account/api-keys
```

**Step 3: Access the Application**
- Open your browser and go to your preview URL
- You should see the NetworkingAI dashboard

**That's it! You're ready to use NetworkingAI.**

---

## 💻 System Requirements

### Minimum Requirements
- **Operating System**: Linux (Ubuntu/Debian preferred)
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **MongoDB**: 4.4 or higher
- **Memory**: 2GB RAM minimum
- **Storage**: 5GB free space

### Recommended Requirements
- **Memory**: 4GB RAM or more
- **CPU**: 2+ cores
- **Storage**: 10GB free space
- **Network**: Stable internet connection for AI features

---

## 🛠️ Installation Guide

### Method 1: Automated Installation (Recommended)

```bash
# Navigate to the project directory
cd /app

# Run the fix/installation script
chmod +x fix-services.sh
./fix-services.sh
```

### Method 2: Manual Installation

#### Backend Setup
```bash
cd /app/backend

# Install Python dependencies
pip install -r requirements.txt

# Install emergentintegrations (for AI features)
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Copy environment file
cp .env.example .env  # Edit with your settings
```

#### Frontend Setup
```bash
cd /app/frontend

# Install Node.js dependencies
yarn install

# Copy environment file
cp .env.example .env  # Edit with your settings
```

#### Start Services
```bash
# Start all services
sudo supervisorctl restart all

# Check status
sudo supervisorctl status
```

---

## ⚙️ Configuration

### 1. Environment Variables

#### Backend Configuration (`/app/backend/.env`)
```bash
# Database Configuration
MONGO_URL="mongodb://localhost:27017"
DB_NAME="networkingai_db"

# AI Configuration (Optional but recommended)
OPENAI_API_KEY=your_openai_api_key_here

# Get your OpenAI key from: https://platform.openai.com/account/api-keys
```

#### Frontend Configuration (`/app/frontend/.env`)
```bash
# Backend URL (usually pre-configured)
REACT_APP_BACKEND_URL=your_backend_url_here
WDS_SOCKET_PORT=443
```

### 2. OpenAI API Key Setup (For AI Email Generation)

1. **Get Your API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
   - Create a new API key
   - Copy the key

2. **Configure the Backend**:
   ```bash
   nano /app/backend/.env
   # Replace: OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
   # With: OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. **Restart Backend**:
   ```bash
   sudo supervisorctl restart backend
   ```

---

## 📱 User Guide

### Dashboard Overview
When you first open NetworkingAI, you'll see:
- **Hero Section**: Welcome message and app description
- **Statistics Cards**: Total contacts, campaigns, response rates, lead scores
- **Recent Contacts**: Your latest added contacts
- **Active Campaigns**: Currently running email campaigns

### 1. Managing Contacts

#### Adding a New Contact
1. Click "Contacts" in the sidebar
2. Click "Add Contact" button
3. Fill in the contact form:
   - **Required**: Name and Email
   - **Optional**: Company, Position, Industry, LinkedIn, Phone, Notes
   - **Priority**: Set to High, Medium, or Low
4. Click "Add Contact"

The system automatically calculates a **Lead Score** (0-100) based on:
- Profile completeness
- Recent interactions
- Contact information quality

#### Viewing and Managing Contacts
- **Contact Cards**: Show name, company, position, email, priority, and lead score
- **Priority Levels**: 
  - 🔴 High Priority (red badge)
  - 🟡 Medium Priority (yellow badge) 
  - 🟢 Low Priority (green badge)
- **Status Tracking**: New → Contacted → Responded → Converted

### 2. AI Email Generation

#### Generating Personalized Emails
1. Click "AI Email Generator" in the sidebar
2. Select a contact from the dropdown
3. Choose email type:
   - **Introduction**: First-time outreach
   - **Follow Up**: Following up on previous contact
   - **Meeting Request**: Requesting a meeting
   - **Thank You**: Thanking for time or opportunity
   - **Reconnection**: Reconnecting after a long time

4. Select tone:
   - **Professional**: Formal business tone
   - **Friendly**: Warm but professional
   - **Casual**: Relaxed and informal
   - **Formal**: Very formal and respectful

5. Add additional context (optional)
6. Click "Generate Email"

#### Using Generated Emails
- **Copy to Clipboard**: Click to copy the complete email
- **Edit as Needed**: Customize the generated content
- **Personalization Notes**: Review AI suggestions for customization

### 3. Contact Discovery

#### Finding New Contacts
1. Click "Contact Discovery" in the sidebar
2. Set search criteria:
   - **Industry**: Target industry (e.g., "Technology")
   - **Role**: Specific job roles (e.g., "Software Engineer")
   - **Company Size**: Startup, Small, Medium, Large
   - **Location**: Geographic location

3. Click "Discover Contacts"
4. Review discovered contacts
5. Click "Add to Contacts" for relevant prospects

### 4. Campaign Management

#### Creating Email Campaigns
1. Click "Campaigns" in the sidebar
2. Click "Create Campaign"
3. Fill in campaign details:
   - **Name**: Campaign name
   - **Description**: Campaign purpose
   - **Contacts**: Select target contacts
   - **Schedule**: Set send time (optional)

4. Click "Create Campaign"

#### Campaign Status
- **Draft**: Being prepared
- **Active**: Currently running
- **Paused**: Temporarily stopped
- **Completed**: Finished running

### 5. Analytics and Insights

#### Performance Metrics
- **Contact Overview**: Total contacts, new contacts this month
- **Email Performance**: Emails sent, responses, conversion rates
- **Contact Distribution**: By status and priority
- **Relationship Scores**: Average lead scores and relationship strength

#### Using Analytics
- Track networking ROI
- Identify most effective outreach strategies
- Monitor relationship development
- Plan future networking activities

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "Preview failed to load" Error

**Solution**:
```bash
# Run the fix script
/app/fix-services.sh

# Or manually restart services
sudo supervisorctl restart all
```

#### 2. AI Email Generation Not Working

**Check 1**: Verify OpenAI API key
```bash
# Edit backend .env file
nano /app/backend/.env
# Ensure OPENAI_API_KEY is set to your actual key
```

**Check 2**: Restart backend after adding key
```bash
sudo supervisorctl restart backend
```

#### 3. Contact Data Not Saving

**Check Database**:
```bash
# Check if MongoDB is running
sudo supervisorctl status mongodb

# Test database connection
curl http://localhost:8001/api/health
```

#### 4. Frontend Not Loading

**Check Frontend Service**:
```bash
# Check if frontend is running
sudo supervisorctl status frontend

# Check for errors
tail -n 20 /var/log/supervisor/frontend.err.log
```

#### 5. Services Keep Crashing

**Check Logs**:
```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log

# Frontend logs  
tail -f /var/log/supervisor/frontend.err.log

# All logs
tail -f /var/log/supervisor/*.log
```

### Emergency Reset

If nothing works, try a complete reset:
```bash
# Stop all services
sudo supervisorctl stop all

# Run fix script
/app/fix-services.sh

# Wait 30 seconds then check
sleep 30
sudo supervisorctl status
```

---

## 🌐 API Documentation

### Health Check Endpoints

#### GET `/api/health`
Comprehensive health check of all systems.

**Response**:
```json
{
  "status": "ok",
  "database": "healthy",
  "emergent_integrations": true,
  "openai_configured": true,
  "timestamp": "2025-01-01T12:00:00"
}
```

### Contact Management

#### POST `/api/contacts`
Create a new contact.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Tech Corp",
  "position": "Developer",
  "priority": "high"
}
```

#### GET `/api/contacts`
Get all contacts with optional filtering.

**Query Parameters**:
- `status`: Filter by contact status
- `priority`: Filter by priority level
- `limit`: Maximum number of results

### AI Email Generation

#### POST `/api/generate-email`
Generate AI-powered personalized email.

**Request Body**:
```json
{
  "contact_id": "contact-uuid",
  "email_type": "introduction",
  "tone": "professional",
  "context": "Following up from conference"
}
```

### Analytics

#### GET `/api/analytics`
Get comprehensive networking analytics.

**Response**:
```json
{
  "total_contacts": 150,
  "email_performance": {
    "response_rate": 25.5,
    "conversion_rate": 12.3
  },
  "relationship_scores": {
    "average_lead_score": 72.4
  }
}
```

---

## 🚀 Deployment Guide

### Production Deployment

#### 1. Environment Setup
```bash
# Set production environment variables
export NODE_ENV=production
export ENVIRONMENT=production

# Configure production database
# Update MONGO_URL in /app/backend/.env
```

#### 2. Build for Production
```bash
# Build frontend
cd /app/frontend
yarn build

# The built files will be in /app/frontend/build/
```

#### 3. Configure Web Server (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Frontend
    location / {
        root /app/frontend/build;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 4. SSL Configuration (Let's Encrypt)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### Docker Deployment (Optional)

#### Dockerfile (Backend)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongo:27017
    depends_on:
      - mongo

  frontend:
    build: ./frontend
    ports:
      - "3000:80"

  mongo:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

---

## 📞 Support and Maintenance

### Regular Maintenance Tasks

#### Weekly
- Check service status: `sudo supervisorctl status`
- Review error logs: `tail /var/log/supervisor/*.log`
- Update dependencies if needed

#### Monthly
- Database backup
- Update system packages
- Review API usage and performance

### Getting Help

1. **Check this guide first** - Most issues are covered here
2. **Run the fix script**: `/app/fix-services.sh`
3. **Check logs** for specific error messages
4. **Test individual components** using the health check endpoint

### Performance Optimization

#### Database Optimization
```bash
# Add indexes for better performance
mongo networkingai_db --eval "
  db.contacts.createIndex({email: 1});
  db.contacts.createIndex({company: 1});
  db.contacts.createIndex({created_at: -1});
"
```

#### Memory Usage
```bash
# Monitor memory usage
free -h
htop

# If running low on memory, restart services
sudo supervisorctl restart all
```

---

## 🎉 Conclusion

You now have a complete understanding of NetworkingAI! This guide covers everything from basic installation to advanced deployment scenarios.

### Key Features Summary
- ✅ **Contact Management**: Add, edit, delete, and organize contacts
- ✅ **AI Email Generation**: Create personalized outreach emails
- ✅ **Contact Discovery**: Find new networking opportunities  
- ✅ **Campaign Management**: Run organized email campaigns
- ✅ **Analytics**: Track networking performance and ROI
- ✅ **Relationship Scoring**: Automatic lead and relationship scoring

### Quick Reference Commands
```bash
# Check service status
sudo supervisorctl status

# Restart all services
sudo supervisorctl restart all

# Run fix script
/app/fix-services.sh

# Check health
curl http://localhost:8001/api/health

# View logs
tail -f /var/log/supervisor/*.log
```

**Happy Networking! 🚀**
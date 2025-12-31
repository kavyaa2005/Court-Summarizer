# MongoDB Setup Guide

## Problem
The Case Record page shows "Connection Error - Could not connect to the server" because MongoDB is not running.

## Solution

### Option 1: Install MongoDB Locally (Recommended)

1. **Download MongoDB Community Server**
   - Visit: https://www.mongodb.com/try/download/community
   - Select: Windows → MSI Installer
   - Download and run the installer

2. **Installation Steps**
   - Choose "Complete" installation
   - Install as a Windows Service (checkbox)
   - Install MongoDB Compass (GUI tool - optional but helpful)

3. **Start MongoDB Service**
   ```powershell
   # Start MongoDB service
   net start MongoDB
   
   # Check if running
   sc query MongoDB
   ```

4. **Verify Connection**
   - Open Command Prompt
   ```bash
   mongosh
   ```
   - Should connect to `mongodb://127.0.0.1:27017`

### Option 2: Use MongoDB Atlas (Cloud - Free)

1. **Create Account**
   - Visit: https://www.mongodb.com/cloud/atlas/register
   - Sign up for free

2. **Create Cluster**
   - Choose FREE tier (M0 Sandbox)
   - Select region closest to you
   - Click "Create Cluster"

3. **Get Connection String**
   - Click "Connect" → "Connect your application"
   - Copy the connection string
   - Example: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`

4. **Update Your Project**
   - Create `.env` file in `db-connect` folder:
   ```env
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/court-summarizer
   PORT=5002
   ```

## After Setup

1. **Restart Node API**
   ```powershell
   cd C:\Users\LENOVO\Desktop\Court-Summarizer\db-connect
   $env:PORT=5002
   node server.js
   ```

2. **You should see:**
   ```
   Connected to MongoDB
   Server running on port 5002
   ```

3. **Test Case Record Page**
   - Go to http://localhost:5173/case-record
   - You should see "No summaries found" instead of connection error
   - Upload a PDF to create your first case record!

## Troubleshooting

### MongoDB Service not starting
```powershell
# Check if already running
netstat -ano | findstr :27017

# If port is in use, kill the process
taskkill /PID <process_id> /F

# Restart service
net stop MongoDB
net start MongoDB
```

### Still getting connection errors
1. Check if MongoDB is listening on port 27017
2. Verify firewall is not blocking MongoDB
3. Try using 127.0.0.1 instead of localhost in connection string

## Current Project Status

✅ **Working:**
- User authentication (signup/login)
- Profile management
- PDF upload & summarization (FastAPI)
- Protected routes

⚠️ **Needs MongoDB:**
- Saving case summaries to database
- Viewing user history in Case Record page
- Downloading/deleting saved summaries

Once MongoDB is running, the entire application will work dynamically with user-specific data!

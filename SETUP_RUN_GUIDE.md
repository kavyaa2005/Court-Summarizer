# Court Summarizer - Setup & Run Guide

## Overview
This is a full-stack legal document summarization platform with:
- **Frontend**: React + Vite (TypeScript-ready)
- **Backend API**: FastAPI (Python) for PDF summarization
- **Backend Server**: Node.js + Express + MongoDB for user management & summaries
- **Authentication**: Persistent login with context-based state management

---

## Prerequisites
- **Python 3.10+** (with venv)
- **Node.js 16+** (npm)
- **MongoDB** (running locally on port 27017)
- **Windows PowerShell 5.1+**

---

## Quick Start (3 Services)

### Terminal 1: FastAPI Server (Port 8000)
```powershell
cd C:\Users\LENOVO\Desktop\Court-Summarizer
& .\.venv\Scripts\Activate.ps1
python -m uvicorn app_final5:app --host 0.0.0.0 --port 8000
```
Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2: Node API Server (Port 5002)
```powershell
cd C:\Users\LENOVO\Desktop\Court-Summarizer\db-connect
$env:PORT=5002; npm start
```
Expected output:
```
Connected to MongoDB
Server running on port 5002
```

### Terminal 3: Frontend (Port 5174)
```powershell
cd C:\Users\LENOVO\Desktop\Court-Summarizer\frontend
npm run dev
```
Expected output:
```
VITE v7.1.3 ready in 479 ms
➜  Local:   http://localhost:5174/
```

---

## Access the App
🌐 **Frontend**: http://localhost:5174

---

## Features

### 🔐 Authentication Flow
1. **Sign Up**: Create account → Auto-logged in → Redirects to Home
2. **Login**: Credentials check → Logged in → Session persists on page reload
3. **Logout**: Click profile dropdown → Logout → Redirected to Login page
4. **Protected Routes**: Unauthenticated users redirected to login

### 👤 User Profile
- View: Full Name, Email, Occupation
- Actions: View Summaries, Logout, Back to Home
- Located at: `http://localhost:5174/profile` (Protected)

### 📄 PDF Upload & Summarization
- Upload legal documents
- FastAPI processes and extracts summaries
- Auto-download JSON summary
- Save summary to database

### 📋 Case Records
- View all saved summaries
- Download summaries
- Delete summaries
- Located at: `http://localhost:5174/case-record` (Protected)

---

## API Endpoints

### FastAPI (Port 8000)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/health` | Health check |
| `POST` | `/summarize_pdf` | Upload & summarize PDF |

### Node API (Port 5002)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/signup` | User registration |
| `POST` | `/api/login` | User login |
| `POST` | `/api/summaries/save` | Save summary to DB |
| `GET` | `/api/summaries/user/:email` | Fetch user's summaries |
| `GET` | `/api/summaries/:id` | Get summary details |
| `DELETE` | `/api/summaries/:id` | Delete summary |

---

## Environment Variables

### Frontend: `frontend/.env`
```
VITE_FASTAPI_URL=http://localhost:8000
VITE_NODE_API_URL=http://localhost:5002/api/summaries
```

---

## Project Structure
```
Court-Summarizer/
├── app_final5.py                 # FastAPI server
├── db-connect/
│   ├── server.js                 # Express server
│   ├── routes/
│   │   ├── auth.js               # Login/Signup routes
│   │   └── summaries.js          # Summary CRUD routes
│   └── models/
│       ├── User.js               # User schema
│       └── Summary.js            # Summary schema
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main app with routing
│   │   ├── context/
│   │   │   └── AuthContext.jsx   # Global auth state
│   │   ├── components/
│   │   │   ├── NavBar.jsx        # Navbar with profile dropdown
│   │   │   ├── ProtectedRoute.jsx# Auth wrapper for routes
│   │   │   ├── Footer.jsx        # Footer
│   │   ├── pages/
│   │   │   ├── Home.jsx          # Home page
│   │   │   ├── Login.jsx         # Login page
│   │   │   ├── Signup.jsx        # Signup page
│   │   │   ├── Profile.jsx       # User profile page
│   │   │   ├── Caserecord.jsx    # Case records page
│   │   │   └── button/
│   │   │       └── Upload.jsx    # PDF upload modal
│   │   ├── assets/
│   │   │   ├── styles/           # CSS files
│   │   │   ├── scripts/          # Helper functions
│   │   │   └── images/           # Images
│   │   └── main.jsx              # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env                      # Environment variables
└── README.md
```

---

## Troubleshooting

### ❌ "FastAPI not reachable"
- **Cause**: FastAPI server not running on port 8000
- **Fix**: Start Terminal 1 with FastAPI command above

### ❌ "Failed to connect to server"
- **Cause**: Node API not running on port 5002 or MongoDB offline
- **Fix**: 
  1. Start Terminal 2 with Node command
  2. Verify MongoDB: `mongod` in another terminal

### ❌ Port already in use
- **FastAPI**: Kill process on 8000 → `netstat -ano | findstr :8000`
- **Node**: Change PORT in Terminal 2 → `$env:PORT=5003; npm start`
- **Frontend**: Auto-increments (5173 → 5174 → 5175...)

### ❌ Module not found
- Run: `npm install` in `frontend/` and `db-connect/`
- For Python: `& .\.venv\Scripts\pip install -r requirements.txt`

---

## Authentication Details

### How Persistent Login Works
1. **On Signup/Login Success**: User object stored in localStorage
2. **On App Load**: AuthContext checks localStorage, restores session
3. **On Page Refresh**: User stays logged in (no re-login needed)
4. **On Logout**: localStorage cleared, redirected to login
5. **Protected Routes**: Check `user` in AuthContext, redirect if null

### User Data Stored
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "occupation": "Lawyer"
}
```

---

## Development Commands

### Frontend
```bash
npm run dev      # Start Vite dev server
npm run build    # Build for production
npm run lint     # Run ESLint
```

### Backend (Node)
```bash
npm start        # Run Express server
npm run dev      # Run with nodemon (auto-restart on changes)
```

### Backend (Python)
```bash
python -m uvicorn app_final5:app --reload --port 8000
```

---

## Common Workflows

### 1️⃣ New User Registration
```
Sign Up → Fill form → Submit → Auto-login → Home page
```

### 2️⃣ Existing User Login
```
Click Sign-In → Enter credentials → Login → Home page
```

### 3️⃣ Upload & Summarize PDF
```
Home → Upload button → Select PDF → Submit → Download JSON summary
```

### 4️⃣ View Profile
```
Navbar → Click name/avatar → Select "My Profile" → View details
```

### 5️⃣ Logout
```
Navbar → Click name/avatar → Select "Logout" → Redirected to Login page
```

---

## Next Steps

### Frontend Enhancements
- [ ] Add profile picture upload
- [ ] Dark mode toggle
- [ ] Email verification
- [ ] Password reset flow
- [ ] Advanced search in case records

### Backend Enhancements
- [ ] JWT tokens for stateless auth
- [ ] Rate limiting on API endpoints
- [ ] File upload size limits
- [ ] Backup & export summaries
- [ ] Advanced PDF parsing

### DevOps
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Production deployment (AWS/Heroku)
- [ ] Environment-based configs

---

## Support
For issues, check browser DevTools (F12) → Console & Network tabs for error details.

---

**Last Updated**: December 27, 2025

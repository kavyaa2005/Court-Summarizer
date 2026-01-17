# 🏛️ Court Summarizer - Legal Document Summarization Platform

A full-stack web application for automated summarization of legal court judgments and documents using advanced NLP techniques.

## 📋 Overview

Court Summarizer is an intelligent legal document processing platform that:
- **Uploads & processes** PDF legal documents
- **Generates summaries** using multiple summarization algorithms
- **Extracts key information** (parties, judges, citations, dates)
- **Saves records** to database for future reference
- **Provides authentication** with persistent user sessions

## ✨ Features

### 🔐 Authentication & User Management
- User registration (Sign up)
- Secure login with password hashing
- Session persistence across page reloads
- User profile management
- Logout functionality

### 📄 Document Processing
- PDF upload support
- Automatic text extraction from legal documents
- Multiple summarization algorithms:
  - **Semantic Chunking** - Context-aware summarization
  - **Token-wise** - Token-based text chunking
  - **Recursive** - Hierarchical document processing
- Metadata extraction (court, case number, parties, judges, dates)
- Citation extraction and analysis

### 📊 Case Records Management
- View all processed summaries
- Download summary JSONs
- Delete saved records
- Track document statistics

### 🎨 User Interface
- Clean, responsive React frontend
- Real-time file upload feedback
- Interactive case record dashboard
- User profile page
- Protected routes (authenticated users only)

## 🛠️ Tech Stack

### Frontend
- **React 19.1.1** - UI framework
- **Vite 7.1.2** - Build tool & dev server
- **React Router v7** - Client-side routing
- **SweetAlert2** - Beautiful alerts
- **GSAP** - Animations

### Backend APIs
- **FastAPI (Python)** - PDF processing & summarization (Port 8000)
- **Node.js + Express** - User auth & database management (Port 5002)

### Database
- **MongoDB** - Store user data and case records (Port 27017)

### Libraries & Tools
- **Transformers** - Pre-trained NLP models
- **Sentence-Transformers** - Semantic embeddings
- **Scikit-learn** - ML algorithms
- **NLTK** - Natural language processing
- **Pandas & NumPy** - Data processing
- **Mongoose** - MongoDB ODM

## 📦 Prerequisites

- **Python 3.10+** with pip
- **Node.js 16+** with npm
- **MongoDB** (Community Edition)
- **Windows PowerShell 5.1+** (for batch scripts)
- **4GB RAM minimum** (8GB recommended for model loading)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Hyphenat/Court-Summarizer.git
cd Court-Summarizer
```

### 2. Run Everything with One Command

**PowerShell:**
```powershell
# Run all services automatically
powershell -NoProfile -ExecutionPolicy Bypass -File "START_ALL.ps1"
```

**OR Manual Setup:**

#### Terminal 1: FastAPI Server (Port 8000)
```powershell
cd C:\Users\fsarg\OneDrive\Desktop\Court-Summarizer
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -q fastapi uvicorn pandas numpy nltk transformers sentence-transformers scikit-learn python-multipart matplotlib textstat
python -m uvicorn app_final5:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2: Node.js Backend (Port 5002)
```powershell
cd Court-Summarizer\db-connect
npm install
$env:PORT=5002
npm start
```

#### Terminal 3: React Frontend (Port 5174)
```powershell
cd Court-Summarizer\frontend
npm install
npm run dev
```

### 3. Start MongoDB (Windows)
```powershell
# If installed as Windows service
net start MongoDB

# Or check status
Get-Service MongoDB | Select-Object Status, Name
```

### 4. Access the Application
🌐 **Frontend:** http://localhost:5174

📚 **FastAPI Docs:** http://localhost:8000/docs

## 📁 Project Structure

```
Court-Summarizer/
├── app_final5.py                 # FastAPI main application
├── db-connect/                   # Node.js backend
│   ├── server.js                # Express server
│   ├── routes/                  # API endpoints
│   │   ├── auth.js             # Authentication
│   │   └── summaries.js        # Summary management
│   ├── models/                 # MongoDB schemas
│   │   ├── User.js
│   │   └── Summary.js
│   └── package.json
├── frontend/                     # React application
│   ├── src/
│   │   ├── App.jsx             # Main component
│   │   ├── pages/              # Page components
│   │   ├── components/         # Reusable components
│   │   └── context/            # Auth context
│   ├── package.json
│   └── vite.config.js
├── Legal-Document-Summarizer/   # ML models & metadata
│   ├── legal_analysis_env/      # Python environment
│   ├── metadata/                # Case metadata
│   └── Original-Judgements/     # Sample judgments
└── README.md
```

## 🔌 API Endpoints

### FastAPI (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/summarize_pdf` | Upload PDF & get summary |

**Upload PDF Example:**
```bash
curl -X POST "http://localhost:8000/summarize_pdf" \
  -F "file=@document.pdf"
```

### Node.js Backend (Port 5002)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/signup` | User registration |
| `POST` | `/api/login` | User login |
| `GET` | `/api/summaries` | Get user's summaries |
| `POST` | `/api/summaries` | Save new summary |
| `DELETE` | `/api/summaries/:id` | Delete summary |

## 🔄 User Flow

### 1. **Sign Up**
```
User fills form → Submit → Account created → Auto-login → Redirected to Home
```

### 2. **Upload & Summarize**
```
Home Page → Select PDF → Upload → FastAPI processes → Summary downloaded → Save to DB
```

### 3. **View Case Records**
```
Case Record Page → List all summaries → Download/Delete options → Manage library
```

### 4. **User Profile**
```
Profile Icon → View info → Logout → Redirected to Login
```

## ⚙️ Configuration

### MongoDB Connection
Edit `db-connect/.env`:
```
MONGODB_URI=mongodb://localhost:27017/court-summarizer
PORT=5002
```

### FastAPI Settings
In `app_final5.py`:
- Port: 8000
- Host: 0.0.0.0 (accessible externally)
- Auto-reload: Enabled for development

### Frontend Dev Server
In `frontend/vite.config.js`:
- Port: 5174
- Hot Module Replacement: Enabled

## 🐛 Troubleshooting

### ❌ FastAPI not running on port 8000?
```powershell
# Check if port is in use
netstat -ano | findstr "8000"

# Kill process on port 8000
taskkill /PID <PID> /F

# Reinstall dependencies
pip install -q fastapi uvicorn matplotlib textstat
```

### ❌ MongoDB connection error?
```powershell
# Start MongoDB service
net start MongoDB

# Or check if already running
Get-Service MongoDB | Select-Object Status
```

### ❌ Node backend won't start?
```powershell
cd db-connect
npm install
npm start
```

### ❌ Frontend shows "API not responding"?
- Ensure FastAPI and Node backends are running
- Check ports 8000 and 5002 are listening
- Clear browser cache: `Ctrl+Shift+Delete`

## 📊 Performance Tips

- **First load** may take 30-60 seconds (model download)
- **NLTK data** auto-downloads on first run
- **Transformers models** cached locally after first use
- Use **8GB+ RAM** for optimal performance

## 🔒 Security Notes

- Passwords hashed with **bcryptjs**
- CORS enabled for local frontend
- Environment variables used for MongoDB URI
- Session persistence via MongoDB

## 📝 Example Workflow

1. Open http://localhost:5174
2. Click "Sign Up"
3. Fill form → Create account
4. Upload a legal PDF document
5. Wait for summarization (30-60 seconds)
6. Download JSON summary
7. View in "Case Records"
8. Delete or download as needed

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Authors

- **Farhan Sargath** - Development & Deployment
- **Kavya** - Original Repository

## 📧 Support

For issues or questions:
- Create an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🚀 Future Enhancements

- [ ] Support for multiple document formats (DOCX, TXT)
- [ ] Batch processing for multiple PDFs
- [ ] Advanced comparison tools
- [ ] Export to different formats (PDF, DOCX)
- [ ] API rate limiting & authentication
- [ ] Docker deployment support
- [ ] Mobile app version
- [ ] Real-time collaboration features

---

**Happy Summarizing!** 🎉

For detailed setup guide, see [SETUP_RUN_GUIDE.md](SETUP_RUN_GUIDE.md)

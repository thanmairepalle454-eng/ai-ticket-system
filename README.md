# 🎫 AI Ticket System

An intelligent ticket management system that uses RAG (Retrieval Augmented Generation) to automatically suggest solutions from a knowledge base.

---

## ✅ What's Fixed

### Problem 1: No UI + Runs only on one system
- ✅ React frontend with Vite
- ✅ Clean UI for raising tickets and uploading PDFs
- ✅ Ready for deployment (instructions below)

### Problem 2: No Knowledge Database for AI
- ✅ RAG system with ChromaDB vector database
- ✅ PDF upload and indexing
- ✅ Semantic search for relevant solutions
- ✅ Sample PDFs included

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install flask flask-cors langchain langchain-community chromadb pypdf sentence-transformers

# Generate sample PDFs (optional)
pip install fpdf2
python create_sample_pdfs.py

# Start backend
python app.py
```

Backend runs on: http://localhost:5000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs on: http://localhost:5173

---

## 📖 How to Use

1. **Upload Knowledge PDFs**
   - Go to "Upload Knowledge PDF" tab
   - Upload IT solution PDFs
   - System will index them automatically

2. **Raise a Ticket**
   - Go to "Raise Ticket" tab
   - Describe your issue (e.g., "VPN not working")
   - Get AI-powered solution instantly

---

## 🌐 Deployment Guide

### Backend Deployment Options

**Option 1: Render**
1. Push code to GitHub
2. Go to render.com
3. Create new Web Service
4. Connect your repo
5. Build command: `pip install -r requirements.txt`
6. Start command: `python app.py`

**Option 2: Railway**
1. Push to GitHub
2. Go to railway.app
3. Deploy from GitHub
4. Add environment variables if needed

**Option 3: AWS EC2**
1. Launch Ubuntu instance
2. Install Python and dependencies
3. Run with gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

### Frontend Deployment

**Vercel (Recommended)**
```bash
cd frontend
npm install -g vercel
vercel
```

**Netlify**
```bash
cd frontend
npm run build
# Upload dist/ folder to Netlify
```

Update API URL in frontend after deployment:
```js
// In vite.config.js, change proxy to your deployed backend URL
```

---

## 📁 Project Structure

```
backend/
  app.py                 # Flask API
  rag_service.py         # RAG logic with ChromaDB
  create_sample_pdfs.py  # Generate sample PDFs
  uploads/               # PDF storage
  chroma_db/             # Vector database

frontend/
  src/
    App.jsx              # Main app
    components/
      TicketForm.jsx     # Ticket submission
      UploadPDF.jsx      # PDF upload
  package.json
  vite.config.js
```

---

## 🧠 How It Works

1. **PDF Upload** → Extract text → Generate embeddings → Store in ChromaDB
2. **Ticket Raised** → Convert to embedding → Search similar solutions → Return best match
3. **AI Response** → User gets step-by-step solution from knowledge base

---

## 🔧 Tech Stack

- **Backend**: Flask, LangChain, ChromaDB, HuggingFace Embeddings
- **Frontend**: React, Vite, Axios
- **AI**: RAG (Retrieval Augmented Generation)
- **Vector DB**: ChromaDB

---

## 📝 Next Steps (Optional Enhancements)

- Add user authentication
- Email notifications (SMTP)
- Admin dashboard
- Ticket status tracking
- PostgreSQL for ticket storage
- OpenAI integration for better responses

---

## 🐛 Troubleshooting

**Backend not starting?**
- Make sure all dependencies are installed
- Check if port 5000 is available

**Frontend can't connect to backend?**
- Ensure backend is running on port 5000
- Check CORS is enabled in Flask

**No solutions found?**
- Upload PDFs first via the UI
- Check if PDFs are in `backend/uploads/`
- Verify ChromaDB is created in `backend/chroma_db/`

---

## 📧 Support

For issues or questions, check the code comments or raise an issue.

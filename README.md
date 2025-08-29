#  AI Powered Document-Summarizer

PDF Insight is a **full-stack web application** that allows you to upload PDF files (e.g., resumes, reports, research papers) and instantly generate **AI-powered summaries** using [Sarvam AI API](https://sarvam.ai).  
If the AI service is unreachable, a **fallback mode** extracts top keywords from the document instead.  
The app also features a **persistent history**, where every upload is saved along with its generated summary — so you can revisit summaries anytime, even years later. 

## ✨ Features

- 📂 **Upload PDFs** (drag & drop / click)  
- 🤖 **AI Summaries** via Sarvam AI  
- 🔑 **Fallback Mode** – Extracts keywords if AI fails  
- 📚 **History Tab** – All uploads saved locally (persistent)  
- 🕒 **View Old Summaries** – Revisit any past upload  
- 🖥 **Modern UI** – Built with HTML, CSS, and Vanilla JS  
- 🗄 **Backend API** – Built with FastAPI + PostgreSQL  

## 🛠 Tech Stack

**Frontend**  
- HTML5  
- CSS3 (responsive UI)  
- JavaScript 
- LocalStorage (persistent history in browser)

**Backend**  
- [FastAPI](https://fastapi.tiangolo.com/) (Python)  
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)  
- [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)  
- [PostgreSQL](https://www.postgresql.org/) (database)  
- [Requests](https://docs.python-requests.org/) (Sarvam AI API calls)  
- [PyPDF2](https://pypi.org/project/pypdf2/) (text extraction from PDFs)

---

## 📂 Project Structure

📦 PDF SUMMARISER
┣ 📂 backend
┃ ┣ main.py # FastAPI entry point
┃ ┣ models.py # SQLAlchemy models
┃ ┣ db.py # Database connection
┃ ┣ sarvam_client.py # Sarvam AI client
┃ ┣ requirements.txt # Python dependencies
┃ ┣ .env
┣ 📂 frontend
┃ ┣ index.html # Main UI
┃ ┣ index.css # Styling
┃ ┣ index.js # Logic for upload, summary, history
┣ README.md # Project documentation


---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repo
```bash
git clone https://github.com/Krishidevgithub/Document-Summarizer.git
cd Document-Summariser

2️⃣ Backend Setup
Create Virtual Environment
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux

Install Dependencies
pip install -r requirements.txt

Requirements (requirements.txt)
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-multipart
requests
pypdf2
python-dotenv

3️⃣ Database Setup (PostgreSQL)

Install PostgreSQL on your system.

Create a database:
CREATE DATABASE pdf_insight_db;

Update your DATABASE_URL in db.py:

DATABASE_URL = "postgresql+psycopg2://pdf_user:yourpassword@localhost/pdf_insight_db"

4️⃣ Database Tables

We’re using SQLAlchemy models, but here’s the raw SQL if you want to create tables manually:

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    insight_type VARCHAR(50) NOT NULL,   -- "ai" or "fallback"
    summary_text TEXT,
    top_words TEXT
);


This table stores every uploaded PDF + its summary/keywords.

5️⃣ Environment Variables

Create a .env file inside backend/:

SARVAM_API_KEY=your_api_key_here
DATABASE_URL = "postgresql+psycopg2://pdf_user:yourpassword@localhost/pdf_insight_db"
SARVAM_BASE=https://api.sarvam.ai/v1

6️⃣ Run Backend
uvicorn main:app --reload --port 8000

Backend will be live at 👉 http://localhost:8000

7️⃣ Frontend Setup

No framework needed! Just open the file:

cd frontend
start index.html        # Windows
open index.html         # Mac


Or serve via simple HTTP server:

python -m http.server 5500

Frontend 👉 http://localhost:5500

OR Simply go to index.html in your folder nd run it using live server(RECOMMENDED)

🔗 API Endpoints
POST /upload-resume

Upload a PDF and get a summary.

Request:
multipart/form-data with a file.

Response:

{
  "summary": "Concise AI summary...",
  "top_words": ["python", "ml", "fastapi"]
}

GET /

Simple health check.

🧪 How to Use

Navigate to Home.

Upload a PDF → Click Generate Summary.

See AI Summary (or fallback keywords).

Navigate to History → Click Show Summary for past uploads.

📖 Example Workflow

Upload resume.pdf.

AI generates:

Experienced Python developer with focus on FastAPI, ML, and cloud services.


Saved in history as:

📄 resume.pdf

Summary available anytime via "Show Summary".

🔮 Future Improvements

Store summaries directly in PostgreSQL instead of localStorage

User authentication (login/signup)

Multi-language summarization

Export summary as PDF/Word

Deploy Backend (Render/Heroku) + Frontend (Vercel/Netlify)


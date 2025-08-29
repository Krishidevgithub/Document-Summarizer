# main.py
import os
import json
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from db import SessionLocal, engine
from models import Base, Document
from utils import extract_text_from_pdf, fallback_top_words
from sarvam_client import summarize_with_sarvam, SarvamError

# Single FastAPI instance
app = FastAPI(title="PDF Summariser API", version="1.0.0")

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]


# Enable CORS (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Storage directory for PDFs
STORAGE_DIR = "./storage"
os.makedirs(STORAGE_DIR, exist_ok=True)


def save_file(upload_file: UploadFile):
    """Save uploaded PDF to storage directory."""
    ext = os.path.splitext(upload_file.filename)[1]
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{ext}"
    path = os.path.join(STORAGE_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return path, filename


@app.get("/")
def root():
    return {"message": "Backend running"}

import time
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload PDF, extract text, summarize, fallback to top words if needed."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    path, filename = save_file(file)

    # Extract text from PDF
    text = extract_text_from_pdf(path)
    if not text.strip():
        raise HTTPException(status_code=400, detail="PDF has no extractable text")

    insight_type = "fallback"
    summary_text = None
    top_words = None


    try:
        
        max_chars = 100000
        safe_text = text[:max_chars]
        summary_text = summarize_with_sarvam(safe_text)
        insight_type = "ai"
    except SarvamError:
        top_words = fallback_top_words(text, top_n=5)

    # Save document to DB
    db = SessionLocal()
    try:
        doc = Document(
            filename=filename,
            storage_path=path,
            insight_type=insight_type,
            summary_text=summary_text,
            top_words=json.dumps(top_words) if top_words else None,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        response = {
            "id": doc.id,
            "filename": filename,
            "insight_type": insight_type,
            "summary": summary_text,
            "top_words": top_words,
        }
        print("Upload response:", response)  # Debug print
        return JSONResponse(content=response)
    finally:
        db.close()


@app.get("/history")
def history():
    """Return all uploaded documents."""
    db = SessionLocal()
    try:
        docs = db.query(Document).order_by(Document.created_at.desc()).all()
        out = [
            {
                "id": d.id,
                "filename": d.filename,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "insight_type": d.insight_type,
            }
            for d in docs
        ]
    finally:
        db.close()
    return out


@app.get("/insights/{doc_id}")
def insights(doc_id: int):
    """Fetch details of a specific document by ID."""
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return {
            "id": doc.id,
            "filename": doc.filename,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
            "insight_type": doc.insight_type,
            "summary": doc.summary_text,
            "top_words": json.loads(doc.top_words) if doc.top_words else None,
        }
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

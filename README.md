# ATS Resume Scorer

A semantic resume-job description matcher using sentence transformers. Unlike keyword-based ATS systems, this tool understands **meaning** � so 'built ML pipelines' matches 'MLOps experience' even without exact word overlap.

## Live Demo
> Coming soon � deploying to Render

## How It Works

1. Upload your resume as a PDF
2. Paste the job description
3. Get a semantic similarity score, matched keywords, and missing skills

Traditional ATS tools use TF-IDF keyword matching. This tool uses \ll-MiniLM-L6-v2\ sentence embeddings to compare meaning in vector space � a fundamentally more accurate approach.

## Tech Stack

- **NLP**: sentence-transformers (HuggingFace), spaCy
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **PDF Parsing**: pdfplumber
- **Containerization**: Docker

## Architecture

\\\
PDF Resume --+
             +--? Text Extraction (pdfplumber)
Job Description --+
                    �
                    ?
         Sentence Embeddings (MiniLM-L6-v2)
                    �
                    ?
         Cosine Similarity Score
                    �
                    ?
         Keyword Gap Analysis (spaCy)
                    �
                    ?
         JSON Response via FastAPI
\\\

## Run Locally

\\\ash
# Clone the repo
git clone https://github.com/AdityaBiswas-ctrl/ats-resume-scorer.git
cd ats-resume-scorer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Start the API
uvicorn app.main:app --reload

# In a second terminal, start the UI
streamlit run streamlit_app.py
\\\

API docs available at: \http://localhost:8000/docs\

## Run with Docker

\\\ash
docker build -t ats-scorer .
docker run -p 8000:8000 ats-scorer
\\\

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /health | GET | Health check |
| /score | POST | Score resume against JD |

## Sample Response

\\\json
{
  "status": "success",
  "similarity_score": 73.4,
  "rating": "Good Match",
  "matched_keywords": ["python", "fastapi", "machine", "learning"],
  "missing_keywords": ["kubernetes", "mlflow", "terraform"]
}
\\\

## Why Semantic Matching?

| Approach | Resume says | JD says | Match? |
|----------|-------------|---------|--------|
| Keyword (TF-IDF) | built ML pipelines | MLOps experience | ? No |
| Semantic (this tool) | built ML pipelines | MLOps experience | ? Yes |

## Author

**Aditya Kr Biswas** � [GitHub](https://github.com/AdityaBiswas-ctrl) 

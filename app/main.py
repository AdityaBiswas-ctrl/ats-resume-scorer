from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.scorer import analyze_match
from app.utils import extract_text_from_pdf, clean_text

app = FastAPI(
    title='ATS Resume Scorer',
    description='Semantic resume-JD matching using sentence transformers',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
async def health_check():
    return {'status': 'ok', 'message': 'ATS Scorer is running'}

@app.post('/score')
async def score_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume_file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are accepted.')

    if not job_description.strip():
        raise HTTPException(status_code=400, detail='Job description cannot be empty.')

    pdf_bytes = await resume_file.read()

    try:
        resume_text = extract_text_from_pdf(pdf_bytes)
        resume_text = clean_text(resume_text)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f'Could not extract text from PDF: {str(e)}')

    if not resume_text:
        raise HTTPException(status_code=422, detail='PDF appears to contain no extractable text.')

    result = analyze_match(resume_text, job_description)

    return {
        'status': 'success',
        'filename': resume_file.filename,
        **result
    }

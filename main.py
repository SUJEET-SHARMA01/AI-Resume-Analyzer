import os
from fastapi import FastAPI, Query, UploadFile, File
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from io import BytesIO

load_dotenv()

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"message":"hello world"}


@app.get("/ask-ai")
def ask_ai(question: str = Query(...)):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question
    )
    return {
        "question" : question,
        "response" : response.text
    }

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    pdf = await file.read()
    reader = PdfReader(BytesIO(pdf))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return {
        "filename" : file.filename,
        "content_type" : file.content_type,
        "text" : text
    }


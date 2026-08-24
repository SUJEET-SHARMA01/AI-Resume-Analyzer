import os
from fastapi import FastAPI,Query
from dotenv import load_dotenv
from google import genai

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
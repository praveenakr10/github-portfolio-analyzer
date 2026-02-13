from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "GitHub Portfolio Analyzer Running 🚀"}

@app.get("/test-groq")
def test_groq():
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )

    response = client.chat.completions.create(
       model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a recruiter."},
            {"role": "user", "content": "Say hello in one line."}
        ]
    )

    return {"response": response.choices[0].message.content}

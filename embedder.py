import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')
MODEL = 'gemini-embedding-001'
MAX_CHARS = 20000
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:embedContent"


def truncate(text: str) -> str:
    return text[:MAX_CHARS]


def get_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        return [0.0] * 3072
    clean = truncate(text.replace('\n', ' '))
    resp = requests.post(
        URL,
        params={"key": API_KEY},
        json={"model": f"models/{MODEL}", "content": {"parts": [{"text": clean}]}}
    )
    resp.raise_for_status()
    return resp.json()["embedding"]["values"]


def embed_resume_sections(sections: dict) -> dict:
    return {
        'skills':     get_embedding(sections.get('skills', '')),
        'experience': get_embedding(sections.get('experience', '')),
        'education':  get_embedding(sections.get('education', '')),
    }

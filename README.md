# AI Resume Screener

Streamlit app that ranks candidates by semantic similarity against a job description using Google Gemini embeddings and cosine similarity scoring.

## Features

- Upload multiple PDF resumes at once
- Paste any job description
- Semantic matching across Skills, Experience, and Education sections
- Weighted overall score per candidate
- Ranked leaderboard table
- CSV export of results
- Scanned/image-only PDF detection and warning

## How It Works

1. Job description is embedded using Gemini `gemini-embedding-001`
2. Each resume PDF is parsed with `pdfplumber` and split into three sections (skills, experience, education) via regex header detection
3. Each section is embedded separately using the same Gemini model
4. Cosine similarity is computed between the JD embedding and each section embedding
5. A weighted overall score is calculated per candidate
6. Candidates are ranked highest to lowest

### Scoring Weights

| Section    | Weight |
|------------|--------|
| Experience | 40%    |
| Skills     | 35%    |
| Education  | 25%    |

## Tech Stack

| Layer        | Technology |
|--------------|------------|
| UI           | Streamlit  |
| PDF Parsing  | pdfplumber, pdfminer.six |
| Embeddings   | Google Gemini API (`gemini-embedding-001`, 3072-dim) |
| Similarity   | scikit-learn cosine similarity |
| Data Export  | pandas |
| HTTP Client  | requests |
| Env Config   | python-dotenv |
| Runtime      | Python 3.12 |

## Project Structure

```
resume-screener/
├── app.py          # Streamlit UI and orchestration
├── parser.py       # PDF text extraction and section chunking
├── embedder.py     # Gemini REST API embedding calls
├── scorer.py       # Cosine similarity + weighted scoring
├── exporter.py     # DataFrame and CSV serialization
├── .env            # API keys (not committed)
└── requirements.txt
```

## Setup

1. Clone the repo and install dependencies:

```bash
pip install streamlit pdfplumber scikit-learn pandas python-dotenv requests
```

2. Create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com).

3. Run the app:

```bash
streamlit run app.py
```

## Keywords

resume screening, AI hiring tool, semantic search, NLP recruitment, cosine similarity, Gemini embeddings, vector similarity, job description matching, candidate ranking, PDF parsing, Streamlit app, Python AI, Google Generative AI, text embeddings, HR automation, ATS alternative

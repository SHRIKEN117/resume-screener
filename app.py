import streamlit as st
import os
from dotenv import load_dotenv
from parser   import parse_resume
from embedder import get_embedding, embed_resume_sections
from scorer   import score_candidate, rank_candidates
from exporter import to_dataframe, to_csv_bytes
 
load_dotenv()
 
# ── Page config ─────────────────────────────────────────────────
st.set_page_config(page_title="Resume Screener", page_icon="U0001F4CB", layout="wide")
st.title("U0001F4CB AI Resume Screener")
st.caption("Rank candidates by semantic match against a job description")
st.divider()
 
# ── Input section ───────────────────────────────────────────────
col1, col2 = st.columns([1, 1])
 
with col1:
    st.subheader("Job Description")
    jd_text = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="We are looking for a Python developer with experience in..."
    )
 
with col2:
    st.subheader("Resume PDFs")
    uploaded_files = st.file_uploader(
        "Upload one or more resumes",
        type=["pdf"],
        accept_multiple_files=True
    )
 
# ── Run button ──────────────────────────────────────────────────
run = st.button(
    "U0001F50D  Screen Candidates",
    disabled=not (jd_text and uploaded_files),
    type="primary"
)
 
# ── Core logic (only runs when button is clicked) ───────────────
if run:
    candidates = []
    warnings  = []
 
    # 1. Embed the job description
    with st.spinner("Embedding job description..."):
        jd_embedding = get_embedding(jd_text)
 
    # 2. Process each uploaded resume
    progress = st.progress(0, text='Processing resumes...')
    for i, pdf_file in enumerate(uploaded_files):
        progress.progress((i+1)/len(uploaded_files),
                          text=f"Processing {pdf_file.name}...")
 
        parsed = parse_resume(pdf_file)
        name   = pdf_file.name.replace('.pdf', '')
 
        if parsed['scanned']:
            warnings.append(name)
            continue
 
        embeddings = embed_resume_sections(parsed['sections'])
        scores     = score_candidate(jd_embedding, embeddings)
        candidates.append({
            'name':     name,
            'scores':   scores,
            'raw_text': parsed['raw_text'],
            'sections': parsed['sections'],
        })
 
    progress.empty()
 
    # 3. Show scanned PDF warnings
    for w in warnings:
        st.warning(f"⚠️ {w} appears to be a scanned PDF. Skipped.")
 
    if not candidates:
        st.error("No valid resumes could be processed.")
        st.stop()
 
    # 4. Rank and display
    ranked = rank_candidates(candidates)
 
    st.divider()
    st.subheader(f"U0001F3C6  Results — {len(ranked)} candidates ranked")
 
    # 5. Leaderboard table
    df = to_dataframe(ranked)
    st.dataframe(df, use_container_width=True, hide_index=True)
 
    # 6. CSV export
    st.download_button(
        label="⬇️  Download results as CSV",
        data=to_csv_bytes(df),
        file_name="screened_candidates.csv",
        mime="text/csv"
    )
    st.divider()
 
    # 7. Per-candidate detail expanders
    st.subheader("Candidate Detail")
    for c in ranked:
        overall = c['scores']['overall']
        with st.expander(f"{c['name']}  —  {overall}% match"):
            m1, m2, m3 = st.columns(3)
            m1.metric('Skills',     f"{c['scores']['skills']}%")
            m2.metric('Experience', f"{c['scores']['experience']}%")
            m3.metric('Education',  f"{c['scores']['education']}%")
            st.progress(int(overall))
            st.caption("Raw extracted text:")
            st.text(c['raw_text'][:1500])

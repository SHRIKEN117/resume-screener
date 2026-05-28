import pdfplumber
import re
 
 
def extract_text(pdf_file) -> str:
    """Extract all text from a PDF file object."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF parse error: {e}")
    return text.strip()
 
 
def chunk_sections(text: str) -> dict:
    """Split resume text into skills, experience, education blocks."""
    # Regex pattern: split on section headers (handles caps/mixed case)
    #pattern = r'(?i)\n(?=(?:SKILLS|TECHNICAL SKILLS|EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|EDUCATION|ACADEMIC))', flags=re.IGNORECASE
    parts = re.split(
        r'(?i)\n(?=(?:SKILLS|TECHNICAL SKILLS|EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|EDUCATION|ACADEMIC))',
        text
    )
 
    sections = {'skills': '', 'experience': '', 'education': ''}
 
    for part in parts:
        part_lower = part.lower()
        if any(k in part_lower for k in ['skill', 'technical']):
            sections['skills'] += part
        elif any(k in part_lower for k in ['experience', 'work', 'employment']):
            sections['experience'] += part
        elif any(k in part_lower for k in ['education', 'academic']):
            sections['education'] += part
 
    # Fallback: if section detection failed, use full text for all
    if not any(sections.values()):
        sections = {'skills': text, 'experience': text, 'education': text}
 
    return sections
 
 
def parse_resume(pdf_file) -> dict:
    """Main entry point. Returns sections dict + raw text + warning flag."""
    raw_text = extract_text(pdf_file)
 
    # Detect scanned/image-only PDFs
    if len(raw_text.strip()) < 50:
        return {
            "sections": {"skills": "", "experience": "", "education": ""},
            "raw_text": "",
            "scanned": True
        }
 
    sections = chunk_sections(raw_text)
    return {
        "sections": sections,
        "raw_text": raw_text,
        "scanned": False
    }

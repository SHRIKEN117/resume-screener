import pandas as pd
import io
 
 
def to_dataframe(candidates: list[dict]) -> pd.DataFrame:
    """Convert ranked candidates list to a flat DataFrame."""
    rows = []
    for i, c in enumerate(candidates):
        rows.append({
            'Rank':           i + 1,
            'Candidate':      c['name'],
            'Overall %':      c['scores']['overall'],
            'Skills %':       c['scores']['skills'],
            'Experience %':   c['scores']['experience'],
            'Education %':    c['scores']['education'],
        })
    return pd.DataFrame(rows)
 
 
def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Serialize DataFrame to CSV bytes for Streamlit download."""
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()

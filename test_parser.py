from parser import parse_resume
 
with open("Shriken_Patel_DA.pdf", "rb") as f:
    result = parse_resume(f)
    print("Scanned:", result["scanned"])
    for section, text in result["sections"].items():
        print(f"\n--- {section.upper()} ({len(text)} chars) ---")
        print(text[:200])

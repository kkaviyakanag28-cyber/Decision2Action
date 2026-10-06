import os, re
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw")
OUT = os.path.join(BASE, "data", "processed")
os.makedirs(OUT, exist_ok=True)

OWNER_PATTERNS = [
    r"(Data Engineering Team)", r"(Analytics Team)", r"(Project Manager)",
    r"(Development Team)", r"(QA Team)", r"(Consulting Team)"
]

def find_owner(text):
    for p in OWNER_PATTERNS:
        m = re.search(p, text, re.I)
        if m:
            return m.group(1)
    return ""

def find_deadline(text):
    patterns = [
        r"\b(September\s+\d{1,2})\b", r"\b(October\s+\d{1,2})\b",
        r"\b(\d{4}-\d{2}-\d{2})\b", r"\b(next week)\b", r"\b(next month)\b"
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return m.group(1)
    return ""

def is_action(text):
    words = ["must", "will", "should", "complete", "migrate", "validate",
             "prepare", "review", "implement", "deliver", "finish", "agreed"]
    return any(w in text.lower() for w in words)

def confidence(text, owner, deadline):
    score = 50
    if is_action(text): score += 20
    if owner: score += 15
    if deadline: score += 15
    return min(score, 100)

def extract():
    df = pd.read_csv(os.path.join(RAW, "meeting_transcripts.csv"))
    rows = []
    for _, r in df.iterrows():
        text = str(r["transcript"])
        if not is_action(text):
            continue
        owner = find_owner(text)
        deadline = find_deadline(text)
        rows.append({
            "action_id": f"ACT-{len(rows)+1:05d}",
            "source_id": r["meeting_id"],
            "timestamp": r["timestamp"],
            "evidence": text,
            "action": text,
            "owner": owner,
            "deadline": deadline,
            "confidence": confidence(text, owner, deadline),
            "status": "HUMAN_CONFIRMATION_REQUIRED" if confidence(text, owner, deadline) >= 70 else "NEEDS_REVIEW"
        })
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(OUT, "extracted_actions.csv"), index=False)
    return out

if __name__ == "__main__":
    result = extract()
    print(f"Extracted actions: {len(result)}")

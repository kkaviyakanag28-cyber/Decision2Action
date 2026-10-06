import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFILE = os.path.join(BASE, "data", "processed", "extracted_actions.csv")
OUTFILE = os.path.join(BASE, "data", "processed", "rule_evaluated_actions.csv")

def evaluate():
    df = pd.read_csv(INFILE)
    scores, triggers, recommendations = [], [], []
    for _, r in df.iterrows():
        score = 0
        rules = []
        text = str(r["evidence"]).lower()
        if any(x in text for x in ["decided", "decision", "agreed", "must", "will"]):
            score += 25; rules.append("DECISION_LANGUAGE")
        if any(x in text for x in ["complete", "migrate", "validate", "prepare", "review"]):
            score += 25; rules.append("ACTION_LANGUAGE")
        if str(r["owner"]).strip():
            score += 25; rules.append("OWNER_IDENTIFIED")
        if str(r["deadline"]).strip():
            score += 25; rules.append("DEADLINE_IDENTIFIED")
        scores.append(score)
        triggers.append(", ".join(rules))
        recommendations.append(
            "READY_FOR_HUMAN_APPROVAL" if score >= 75 else "NEEDS_HUMAN_REVIEW"
        )
    df["rule_score"] = scores
    df["rules_triggered"] = triggers
    df["recommendation"] = recommendations
    df.to_csv(OUTFILE, index=False)
    return df

if __name__ == "__main__":
    result = evaluate()
    print(result[["action_id","rule_score","recommendation"]].to_string(index=False))

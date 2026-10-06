import os, pandas as pd
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
inp=os.path.join(BASE,"data","processed","rule_evaluated_actions.csv")
out=os.path.join(BASE,"data","processed","error_analysis.csv")
df=pd.read_csv(inp)
result=pd.DataFrame({
    "action_id":df["action_id"],
    "low_confidence":df["confidence"] < 70,
    "missing_owner":df["owner"].fillna("").astype(str).str.strip().eq(""),
    "missing_deadline":df["deadline"].fillna("").astype(str).str.strip().eq(""),
    "needs_review":df["recommendation"].eq("NEEDS_HUMAN_REVIEW")
})
result.to_csv(out,index=False)
print(result.sum(numeric_only=True))
print("Saved:",out)

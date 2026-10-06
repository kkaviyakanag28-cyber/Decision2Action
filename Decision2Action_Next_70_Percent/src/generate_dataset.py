import os, random, pandas as pd
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(BASE,"data","raw"); os.makedirs(RAW,exist_ok=True)
random.seed(42)
owners=["Data Engineering Team","Analytics Team","Project Manager","Development Team","QA Team","Consulting Team",""]
deadlines=["Friday","next Monday","next week","30 October 2026",""]
templates=[
"Decision made: approve the dashboard redesign. {owner} will complete the API update by {deadline}.",
"The team agreed to migrate the reporting pipeline. {owner} should prepare the migration checklist by {deadline}.",
"Action item: {owner} will validate the client data and share results by {deadline}.",
"Discussion only: several options were reviewed, but no final decision was made."
]
rows=[]
for i in range(1,10001):
    owner=random.choice(owners); deadline=random.choice(deadlines)
    rows.append({"source_id":f"SRC-{i:05d}","source_type":random.choice(["meeting","chat"]),
                 "text":random.choice(templates).format(owner=owner or "the assigned team",deadline=deadline or "the agreed date"),
                 "impact":random.choice(["LOW","MEDIUM","HIGH"])})
df=pd.DataFrame(rows)
parts=[("meeting_transcripts.csv",0,7000),("chat_threads.csv",7000,8500),
       ("decisions.csv",8500,9300),("tasks.csv",9300,9800),("completion_updates.csv",9800,10000)]
for name,a,b in parts: df.iloc[a:b].to_csv(os.path.join(RAW,name),index=False)
print("Generated 10,000 source records.")

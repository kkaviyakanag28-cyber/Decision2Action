import os,sqlite3,pandas as pd
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB=os.path.join(BASE,"database","decision2action.db"); CSV=os.path.join(BASE,"data","processed","rule_evaluated_actions.csv")
c=sqlite3.connect(DB); q=c.cursor()
q.executescript('''CREATE TABLE IF NOT EXISTS actions(id INTEGER PRIMARY KEY,action_id TEXT UNIQUE,source_id TEXT,evidence TEXT,owner TEXT,deadline TEXT,impact TEXT,confidence REAL,rule_score INTEGER,recommendation TEXT,status TEXT);
CREATE TABLE IF NOT EXISTS audit_log(id INTEGER PRIMARY KEY,action_id TEXT,event TEXT,details TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);''')
df=pd.read_csv(CSV)
for _,r in df.iterrows():
 q.execute("INSERT OR REPLACE INTO actions(action_id,source_id,evidence,owner,deadline,impact,confidence,rule_score,recommendation,status) VALUES(?,?,?,?,?,?,?,?,?,?)",
 (r.action_id,r.source_id,r.evidence,r.owner,r.deadline,r.impact,r.confidence,r.rule_score,r.recommendation,r.status))
c.commit(); c.close(); print("Loaded",len(df),"actions.")

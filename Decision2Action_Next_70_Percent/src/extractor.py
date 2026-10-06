import os,re,glob,pandas as pd
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(BASE,"data","raw"); OUT=os.path.join(BASE,"data","processed"); os.makedirs(OUT,exist_ok=True)
owners=["Data Engineering Team","Analytics Team","Project Manager","Development Team","QA Team","Consulting Team"]
def owner(t):
    for x in owners:
        if x and re.search(re.escape(x),t,re.I): return x
    return ""
def deadline(t):
    for x in ["Friday","next Monday","next week","30 October 2026"]:
        if re.search(r"by "+re.escape(x),t,re.I): return x
    return ""
rows=[]
for f in glob.glob(os.path.join(RAW,"*.csv")):
    df=pd.read_csv(f)
    for _,r in df.iterrows():
        t=str(r.get("text",""))
        if not any(k in t.lower() for k in ["decision made","agreed to","action item","will complete","should prepare"]): continue
        o=owner(t); d=deadline(t); c=.55+(.15 if "decision" in t.lower() or "agreed" in t.lower() else 0)+(.15 if o else 0)+(.15 if d else 0)
        rows.append({"action_id":f"ACT-{len(rows)+1:05d}","source_id":r["source_id"],"evidence":t,
                     "owner":o,"deadline":d,"impact":r["impact"],"confidence":min(c,1),
                     "status":"HUMAN_CONFIRMATION_REQUIRED" if r["impact"]=="HIGH" else "NEEDS_REVIEW"})
pd.DataFrame(rows).to_csv(os.path.join(OUT,"extracted_actions.csv"),index=False)
print("Extracted",len(rows),"action candidates.")

import os,sqlite3
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DB=os.path.join(BASE,"database","decision2action.db")
def update(action_id,status,reason=""):
 c=sqlite3.connect(DB); c.execute("UPDATE actions SET status=? WHERE action_id=?",(status,action_id)); c.execute("INSERT INTO audit_log(action_id,event,details) VALUES(?,?,?)",(action_id,status,reason)); c.commit(); c.close()
def approve_action(action_id): update(action_id,"APPROVED","Human confirmation granted.")
def override_action(action_id,reason):
 if not reason.strip(): raise ValueError("Override reason is required.")
 update(action_id,"OVERRIDDEN",reason)

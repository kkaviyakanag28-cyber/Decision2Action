import os, sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "database", "decision2action.db")

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = connect()
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS actions (
        action_id TEXT PRIMARY KEY,
        source_id TEXT,
        evidence TEXT,
        action TEXT,
        owner TEXT,
        deadline TEXT,
        confidence REAL,
        rule_score REAL,
        recommendation TEXT,
        status TEXT
    );
    CREATE TABLE IF NOT EXISTS approvals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_id TEXT,
        decision TEXT,
        reason TEXT,
        timestamp TEXT
    );
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_id TEXT,
        event TEXT,
        details TEXT,
        timestamp TEXT
    );
    """)
    con.commit()
    con.close()

def load_actions(csv_path):
    import pandas as pd
    df = pd.read_csv(csv_path)
    con = connect()
    for _, r in df.iterrows():
        con.execute("""
        INSERT OR REPLACE INTO actions
        (action_id,source_id,evidence,action,owner,deadline,confidence,
         rule_score,recommendation,status)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """, tuple(r.get(c, "") for c in [
            "action_id","source_id","evidence","action","owner","deadline",
            "confidence","rule_score","recommendation","status"]))
    con.commit()
    con.close()

def get_actions():
    con = connect()
    rows = con.execute("SELECT * FROM actions ORDER BY action_id").fetchall()
    cols = [x[0] for x in con.execute("PRAGMA table_info(actions)").fetchall()]
    con.close()
    return [dict(zip(cols, r)) for r in rows]

def update_status(action_id, status, reason=""):
    con = connect()
    con.execute("UPDATE actions SET status=? WHERE action_id=?", (status, action_id))
    con.execute(
        "INSERT INTO approvals(action_id,decision,reason,timestamp) VALUES(?,?,?,?)",
        (action_id, status, reason, datetime.now().isoformat(timespec="seconds"))
    )
    con.execute(
        "INSERT INTO audit_log(action_id,event,details,timestamp) VALUES(?,?,?,?)",
        (action_id, "STATUS_CHANGE", reason, datetime.now().isoformat(timespec="seconds"))
    )
    con.commit()
    con.close()

def get_audit():
    con = connect()
    rows = con.execute("SELECT * FROM audit_log ORDER BY id DESC").fetchall()
    con.close()
    return rows

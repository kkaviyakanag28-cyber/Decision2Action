import os,sqlite3,sys
from flask import Flask,render_template,request,redirect,url_for
BASE=os.path.dirname(os.path.abspath(__file__)); sys.path.append(os.path.join(BASE,"src"))
from approval import approve_action,override_action
DB=os.path.join(BASE,"database","decision2action.db"); app=Flask(__name__)
@app.route("/")
def home():
 c=sqlite3.connect(DB); q=c.cursor()
 vals=[q.execute("SELECT COUNT(*) FROM actions").fetchone()[0],
       q.execute("SELECT COUNT(*) FROM actions WHERE status NOT IN ('APPROVED','OVERRIDDEN')").fetchone()[0],
       q.execute("SELECT COUNT(*) FROM actions WHERE impact='HIGH'").fetchone()[0]]
 c.close(); return render_template("index.html",total=vals[0],pending=vals[1],high=vals[2])
@app.route("/actions")
def actions():
 c=sqlite3.connect(DB); rows=c.execute("SELECT action_id,owner,deadline,impact,confidence,status FROM actions ORDER BY id DESC LIMIT 100").fetchall(); c.close()
 return render_template("actions.html",rows=rows)
@app.route("/review/<aid>")
def review(aid):
 c=sqlite3.connect(DB); row=c.execute("SELECT action_id,source_id,evidence,owner,deadline,impact,confidence,rule_score,recommendation,status FROM actions WHERE action_id=?",(aid,)).fetchone(); c.close()
 return render_template("review.html",row=row)
@app.post("/approve/<aid>")
def approve(aid): approve_action(aid); return redirect(url_for("review",aid=aid))
@app.post("/override/<aid>")
def override(aid): override_action(aid,request.form["reason"]); return redirect(url_for("review",aid=aid))
if __name__=="__main__": app.run(debug=True)

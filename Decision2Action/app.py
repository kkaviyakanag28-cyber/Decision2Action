from flask import Flask, render_template, redirect, url_for, request, flash
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database.database import init_db, get_actions, get_audit
from src.approval import approve_action, override_action

app = Flask(__name__)
app.secret_key = "decision2action-demo"
init_db()

@app.route("/")
def index():
    actions = get_actions()
    return render_template("index.html", actions=actions)

@app.route("/actions")
def actions():
    return render_template("actions.html", actions=get_actions())

@app.route("/review/<action_id>")
def review(action_id):
    action = next((a for a in get_actions() if a["action_id"] == action_id), None)
    if not action:
        return "Action not found", 404
    return render_template("review.html", action=action)

@app.post("/approve/<action_id>")
def approve(action_id):
    approve_action(action_id)
    flash("Action approved successfully.")
    return redirect(url_for("review", action_id=action_id))

@app.post("/override/<action_id>")
def override(action_id):
    reason = request.form.get("reason", "")
    try:
        override_action(action_id, reason)
        flash("Action overridden and reason recorded.")
    except ValueError as e:
        flash(str(e))
    return redirect(url_for("review", action_id=action_id))

@app.route("/audit")
def audit():
    return render_template("audit.html", logs=get_audit())

if __name__ == "__main__":
    print("Starting Flask server...")
    print("Open: http://127.0.0.1:5000")
    app.run(debug=True)

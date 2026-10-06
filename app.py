from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import sys

# Allow importing modules from src
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from approval import approve_action, override_action


app = Flask(__name__)

DATABASE_PATH = "database/decision2action.db"


def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def dashboard():

    db = get_db()

    # Total actions
    total_actions = db.execute(
        "SELECT COUNT(*) FROM actions"
    ).fetchone()[0]

    # Pending review
    pending_review = db.execute("""
        SELECT COUNT(*)
        FROM actions
        WHERE status IN (
            'NEEDS_REVIEW',
            'PENDING_APPROVAL',
            'HUMAN_CONFIRMATION_REQUIRED'
        )
    """).fetchone()[0]

    # High impact
    high_impact = db.execute("""
        SELECT COUNT(*)
        FROM actions
        WHERE impact = 'HIGH'
    """).fetchone()[0]

    # Approved
    approved = db.execute("""
        SELECT COUNT(*)
        FROM actions
        WHERE status = 'APPROVED'
    """).fetchone()[0]

    # Overridden
    overridden = db.execute("""
        SELECT COUNT(*)
        FROM actions
        WHERE status = 'OVERRIDDEN'
    """).fetchone()[0]

    # Recent actions
    actions = db.execute("""
        SELECT *
        FROM actions
        ORDER BY action_id
        LIMIT 20
    """).fetchall()

    db.close()

    return render_template(
        "index.html",
        total_actions=total_actions,
        pending_review=pending_review,
        high_impact=high_impact,
        approved=approved,
        overridden=overridden,
        actions=actions
    )


@app.route("/review/<action_id>")
def review_action(action_id):

    db = get_db()

    action = db.execute("""
        SELECT
            actions.*,
            decisions.evidence,
            decisions.source_id
        FROM actions
        LEFT JOIN decisions
        ON actions.decision_id = decisions.decision_id
        WHERE actions.action_id = ?
    """, (action_id,)).fetchone()

    db.close()

    if action is None:
        return "Action not found", 404

    return render_template(
        "review.html",
        action=action
    )


@app.route("/approve/<action_id>", methods=["POST"])
def approve(action_id):

    approve_action(
        action_id,
        reviewer="Web Reviewer"
    )

    return redirect(
        url_for("review_action", action_id=action_id)
    )


@app.route("/override/<action_id>", methods=["POST"])
def override(action_id):

    reason = request.form.get(
        "reason",
        ""
    ).strip()

    if not reason:

        return "Override reason is required.", 400

    override_action(
        action_id,
        reason,
        reviewer="Web Reviewer"
    )

    return redirect(
        url_for("review_action", action_id=action_id)
    )


@app.route("/actions")
def actions_page():

    db = get_db()

    actions = db.execute("""
        SELECT *
        FROM actions
        ORDER BY action_id
    """).fetchall()

    db.close()

    return render_template(
        "actions.html",
        actions=actions
    )


@app.route("/audit")
def audit_page():

    db = get_db()

    logs = db.execute("""
        SELECT *
        FROM audit_log
        ORDER BY timestamp DESC
        LIMIT 100
    """).fetchall()

    db.close()

    return render_template(
        "audit.html",
        logs=logs
    )


if __name__ == "__main__":

    print("=" * 60)
    print("DECISION2ACTION WEB APPLICATION")
    print("=" * 60)

    print("\nStarting Flask server...")
    print("Open: http://127.0.0.1:5000")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
    
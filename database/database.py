import sqlite3
import os
from datetime import datetime


DATABASE_PATH = "database/decision2action.db"


def get_connection():
    """Create database connection."""

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create all required project tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # Decisions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            decision_id TEXT PRIMARY KEY,
            source_id TEXT,
            decision_text TEXT,
            evidence TEXT,
            confidence INTEGER,
            status TEXT,
            created_at TEXT
        )
    """)

    # Actions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            action_id TEXT PRIMARY KEY,
            decision_id TEXT,
            action_text TEXT,
            owner TEXT,
            deadline TEXT,
            impact TEXT,
            confidence INTEGER,
            status TEXT,
            FOREIGN KEY (decision_id)
                REFERENCES decisions(decision_id)
        )
    """)

    # Human approvals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id TEXT,
            decision TEXT,
            reason TEXT,
            reviewed_at TEXT
        )
    """)

    # Completion updates table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completion_updates (
            update_id TEXT PRIMARY KEY,
            action_id TEXT,
            update_text TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)

    # Audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id TEXT,
            event TEXT,
            old_status TEXT,
            new_status TEXT,
            reason TEXT,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully.")


def insert_decision(
    decision_id,
    source_id,
    decision_text,
    evidence,
    confidence,
    status
):
    """Insert a decision into the database."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO decisions
        (
            decision_id,
            source_id,
            decision_text,
            evidence,
            confidence,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        decision_id,
        source_id,
        decision_text,
        evidence,
        confidence,
        status,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


def insert_action(
    action_id,
    decision_id,
    action_text,
    owner,
    deadline,
    impact,
    confidence,
    status
):
    """Insert an action into the database."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO actions
        (
            action_id,
            decision_id,
            action_text,
            owner,
            deadline,
            impact,
            confidence,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        action_id,
        decision_id,
        action_text,
        owner,
        deadline,
        impact,
        confidence,
        status
    ))

    connection.commit()
    connection.close()


def record_approval(
    action_id,
    decision,
    reason=""
):
    """Store human approval or override."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO approvals
        (
            action_id,
            decision,
            reason,
            reviewed_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        action_id,
        decision,
        reason,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


def record_audit(
    action_id,
    event,
    old_status,
    new_status,
    reason=""
):
    """Store an audit trail entry."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO audit_log
        (
            action_id,
            event,
            old_status,
            new_status,
            reason,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        action_id,
        event,
        old_status,
        new_status,
        reason,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


def update_action_status(
    action_id,
    new_status,
    reason=""
):
    """Update action status and create an audit entry."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM actions
        WHERE action_id = ?
    """, (action_id,))

    result = cursor.fetchone()

    if result is None:
        connection.close()
        return False

    old_status = result[0]

    cursor.execute("""
        UPDATE actions
        SET status = ?
        WHERE action_id = ?
    """, (
        new_status,
        action_id
    ))

    cursor.execute("""
        INSERT INTO audit_log
        (
            action_id,
            event,
            old_status,
            new_status,
            reason,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        action_id,
        "STATUS_CHANGE",
        old_status,
        new_status,
        reason,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()

    return True


def get_action(action_id):
    """Get one action."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM actions
        WHERE action_id = ?
    """, (action_id,))

    result = cursor.fetchone()

    connection.close()

    return result


def get_all_actions():
    """Get all tracked actions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM actions
        ORDER BY deadline
    """)

    results = cursor.fetchall()

    connection.close()

    return results


if __name__ == "__main__":

    initialize_database()

    print("Tables created:")
    print("- decisions")
    print("- actions")
    print("- approvals")
    print("- completion_updates")
    print("- audit_log")
    
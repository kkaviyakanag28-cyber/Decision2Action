import pandas as pd
import sqlite3
import sys
import os

# Allow importing database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import initialize_database


DATABASE_PATH = "database/decision2action.db"

INPUT_FILE = "data/processed/rule_evaluated_actions.csv"


def load_actions_to_database():

    print("=" * 60)
    print("DECISION2ACTION - DATABASE LOADER")
    print("=" * 60)

    # Initialize database tables
    initialize_database()

    # Read processed CSV
    df = pd.read_csv(INPUT_FILE)

    print(f"\nRecords found in processed file: {len(df)}")

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    inserted = 0

    for index, row in df.iterrows():

        # Generate unique IDs
        decision_id = f"DEC-{index + 1:05d}"
        action_id = f"ACT-{index + 1:05d}"

        source_id = str(row.get("source_id", "UNKNOWN"))

        evidence = str(
            row.get("evidence", "")
        )

        owner = str(
            row.get("owner", "UNKNOWN")
        )

        deadline = str(
            row.get("deadline", "UNKNOWN")
        )

        confidence = int(
            row.get("confidence", 0)
        )

        recommendation = str(
            row.get("recommendation", "NEEDS_HUMAN_REVIEW")
        )

        rules = str(
            row.get("rules_triggered", "")
        )

        # Create decision text
        decision_text = evidence

        # Create action text
        action_text = evidence

        # Determine impact
        high_impact_words = [
            "production",
            "security",
            "deployment",
            "migration",
            "financial",
            "delete"
        ]

        if any(
            word in evidence.lower()
            for word in high_impact_words
        ):
            impact = "HIGH"
        else:
            impact = "NORMAL"

        # Determine initial status
        if impact == "HIGH":
            status = "HUMAN_CONFIRMATION_REQUIRED"

        elif recommendation == "READY_FOR_HUMAN_APPROVAL":
            status = "PENDING_APPROVAL"

        else:
            status = "NEEDS_REVIEW"

        # Insert decision
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
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            decision_id,
            source_id,
            decision_text,
            evidence,
            confidence,
            status
        ))

        # Insert action
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

        # Audit entry
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
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (
            action_id,
            "ACTION_CREATED",
            "NONE",
            status,
            f"Rules: {rules}"
        ))

        inserted += 1

    connection.commit()

    # Database statistics
    cursor.execute(
        "SELECT COUNT(*) FROM decisions"
    )
    decision_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM actions"
    )
    action_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM actions
        GROUP BY status
    """)

    status_counts = cursor.fetchall()

    connection.close()

    print("\nDatabase loading completed successfully.")

    print(f"\nDecisions stored: {decision_count}")
    print(f"Actions stored: {action_count}")

    print("\nAction status summary:")

    for status, count in status_counts:
        print(f"{status}: {count}")

    print("\nDatabase:")
    print(DATABASE_PATH)


if __name__ == "__main__":

    load_actions_to_database()
    
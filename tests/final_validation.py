import pandas as pd

INPUT_FILE = "data/processed/rule_evaluated_actions.csv"


def final_validation():

    df = pd.read_csv(INPUT_FILE)

    print("=" * 60)
    print("DECISION2ACTION - FINAL VALIDATION")
    print("=" * 60)

    print(f"\nTotal Actions : {len(df)}")

    print("\nColumns:")
    print(list(df.columns))

    print("\nStatus Distribution:")
    if "status" in df.columns:
        print(df["status"].value_counts(dropna=False))

    print("\nConfidence Distribution:")
    if "confidence" in df.columns:
        print(df["confidence"].value_counts(dropna=False).sort_index())

    print("\nOwner Information:")
    if "owner" in df.columns:
        owner_missing = (
            df["owner"].isna() |
            (df["owner"].astype(str).str.upper() == "UNKNOWN")
        )
        print(f"Missing/Unknown Owner : {owner_missing.sum()}")
        print(f"Owner Identified      : {(~owner_missing).sum()}")

    print("\nDeadline Information:")
    if "deadline" in df.columns:
        deadline_missing = (
            df["deadline"].isna() |
            (df["deadline"].astype(str).str.upper() == "UNKNOWN")
        )
        print(f"Missing/Unknown Deadline : {deadline_missing.sum()}")
        print(f"Deadline Identified      : {(~deadline_missing).sum()}")

    print("\nValidation Checks:")
    print("-" * 60)

    checks = {
        "Dataset loaded": len(df) > 0,
        "Required source_id exists": "source_id" in df.columns,
        "Owner field exists": "owner" in df.columns,
        "Deadline field exists": "deadline" in df.columns,
        "Confidence field exists": "confidence" in df.columns,
        "Status field exists": "status" in df.columns,
    }

    for check, result in checks.items():
        print(f"{check:<35} : {'PASS' if result else 'FAIL'}")

    print("\nFinal validation completed successfully.")


if __name__ == "__main__":
    final_validation()
    
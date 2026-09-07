import pandas as pd

INPUT_FILE = "data/processed/rule_evaluated_actions.csv"
OUTPUT_FILE = "data/processed/error_analysis.csv"


def error_analysis():

    df = pd.read_csv(INPUT_FILE)

    print("=" * 60)
    print("DECISION2ACTION - ERROR ANALYSIS")
    print("=" * 60)

    print(f"\nTotal records: {len(df)}")

    # Missing owner
    missing_owner = df[
        df["owner"].isna() |
        (df["owner"].astype(str).str.upper() == "UNKNOWN")
    ]

    # Missing deadline
    missing_deadline = df[
        df["deadline"].isna() |
        (df["deadline"].astype(str).str.upper() == "UNKNOWN")
    ]

    # High impact
    if "impact" in df.columns:
        high_impact = df[
        df["impact"].astype(str).str.upper() == "HIGH"
    ]
    else:
        high_impact = pd.DataFrame()

    # Low confidence
    low_confidence = df[
        pd.to_numeric(df["confidence"], errors="coerce") < 70
    ]

    # Human review
    human_review = df[
        df["status"].astype(str).str.upper().isin([
            "NEEDS_REVIEW",
            "HUMAN_CONFIRMATION_REQUIRED"
        ])
    ]

    print("\nERROR / EDGE CASE SUMMARY")
    print("-" * 60)

    print(f"Missing Owner              : {len(missing_owner)}")
    print(f"Missing Deadline           : {len(missing_deadline)}")
    print(f"High Impact Actions        : {len(high_impact)}")
    print(f"Low Confidence (<70%)      : {len(low_confidence)}")
    print(f"Human Review Required      : {len(human_review)}")

    # Create analysis labels
    analysis = df.copy()

    analysis["error_type"] = "NORMAL"

    analysis.loc[
        analysis["owner"].isna() |
        (analysis["owner"].astype(str).str.upper() == "UNKNOWN"),
        "error_type"
    ] = "MISSING_OWNER"

    analysis.loc[
        analysis["deadline"].isna() |
        (analysis["deadline"].astype(str).str.upper() == "UNKNOWN"),
        "error_type"
    ] = "MISSING_DEADLINE"

    if "impact" in analysis.columns:
        analysis.loc[
        analysis["impact"].astype(str).str.upper() == "HIGH",
        "error_type"
    ] = "HIGH_IMPACT"

    analysis.loc[
        pd.to_numeric(analysis["confidence"], errors="coerce") < 70,
        "error_type"
    ] = "LOW_CONFIDENCE"

    analysis.to_csv(OUTPUT_FILE, index=False)

    print("\nResults saved to:")
    print(OUTPUT_FILE)

    print("\nError Type Distribution:")
    print(analysis["error_type"].value_counts())

    print("\nError analysis completed successfully.")


if __name__ == "__main__":
    error_analysis()
    
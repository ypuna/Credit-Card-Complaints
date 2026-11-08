"""Optional: rebuild the 2024 credit card subset from the full CFPB complaint export.

Input:  complaints.csv (full CFPB Consumer Complaint Database export, ~5.7 GB)
        Download from consumerfinance.gov > Consumer Complaint Database > Download.
Output: data/cc2024_capone_vs_10_peers.csv (Capital One + 10 peer card issuers, 2024)
Run:    python build_subset.py path/to/complaints.csv
"""
import sys
from pathlib import Path

import pandas as pd

CAP = "CAPITAL ONE FINANCIAL CORPORATION"
PEERS = [
    "CITIBANK, N.A.", "SYNCHRONY FINANCIAL", "JPMORGAN CHASE & CO.",
    "AMERICAN EXPRESS COMPANY", "BANK OF AMERICA, NATIONAL ASSOCIATION",
    "Bread Financial Holdings, Inc.", "DISCOVER BANK", "WELLS FARGO & COMPANY",
    "GOLDMAN SACHS BANK USA", "BARCLAYS BANK DELAWARE",
]
COLS = ["Complaint ID", "Date received", "Product", "Issue", "Sub-issue",
        "Company", "Company response to consumer"]


def main(raw_path):
    out = Path(__file__).parent / "data" / "cc2024_capone_vs_10_peers.csv"
    out.parent.mkdir(exist_ok=True)
    parts = []
    for chunk in pd.read_csv(raw_path, chunksize=500_000, dtype=str, usecols=COLS):
        m = (
            chunk["Product"].isin(["Credit card", "Credit card or prepaid card"])
            & chunk["Date received"].str.startswith("2024")
            & chunk["Company"].isin([CAP] + PEERS)
        )
        if m.any():
            parts.append(chunk[m])
    df = pd.concat(parts)
    df.to_csv(out, index=False)
    print(f"Wrote {len(df):,} rows to {out}")


if __name__ == "__main__":
    main(sys.argv[1])

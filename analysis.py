"""Capital One vs. 10 peer card issuers: 2024 CFPB credit card complaints.

Questions:
1. How concentrated are Capital One's complaints in "card opened without my consent"?
2. On which issues does Capital One give consumers relief less often than peers,
   and how many extra relieved complaints would matching the peer rate produce?

Input:  data/cc2024_capone_vs_10_peers.csv (build with build_subset.py)
Run:    python analysis.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "cc2024_capone_vs_10_peers.csv"
OUT = ROOT / "results"

CAP = "CAPITAL ONE FINANCIAL CORPORATION"
RELIEF = ["Closed with monetary relief", "Closed with non-monetary relief"]
TARGET_SUBISSUE = "Card opened without my consent or knowledge"
MIN_N = 50  # minimum Capital One complaints for an issue to be compared


def main():
    df = pd.read_csv(DATA, dtype=str)
    OUT.mkdir(exist_ok=True)
    df["is_cap"] = df["Company"].eq(CAP)
    df["relief"] = df["Company response to consumer"].isin(RELIEF).astype(int)
    df["target"] = df["Sub-issue"].eq(TARGET_SUBISSUE).astype(int)

    cap, peers = df[df.is_cap], df[~df.is_cap]
    share_cap, share_peer = cap["target"].mean(), peers["target"].mean()

    rows = []
    for issue, g in df.groupby("Issue"):
        c, p = g[g.is_cap], g[~g.is_cap]
        if len(c) >= MIN_N:
            rows.append({
                "issue": issue,
                "capone_complaints": len(c),
                "capone_relief_rate": c["relief"].mean(),
                "peer_relief_rate": p["relief"].mean(),
            })
    issues = pd.DataFrame(rows).sort_values("capone_complaints", ascending=False)
    issues["gap"] = issues["peer_relief_rate"] - issues["capone_relief_rate"]
    issues["extra_relief_if_matched"] = (issues["gap"].clip(lower=0) * issues["capone_complaints"]).round()
    issues.to_csv(OUT / "relief_by_issue.csv", index=False)

    summary = {
        "complaints_total": len(df),
        "companies": int(df["Company"].nunique()),
        "capone_complaints": len(cap),
        "opened_without_consent_share_capone": share_cap,
        "opened_without_consent_share_peers": share_peer,
        "opened_without_consent_ratio": share_cap / share_peer,
        "issues_compared": len(issues),
        "issues_capone_trails": int((issues["gap"] > 0).sum()),
        "extra_relief_if_matched_peer_rates": int(issues["extra_relief_if_matched"].sum()),
        "overall_relief_rate_capone": cap["relief"].mean(),
        "overall_relief_rate_peers": peers["relief"].mean(),
    }
    (OUT / "results.json").write_text(json.dumps(summary, indent=2))

    lines = [
        "# Capital One vs. 10 Peer Card Issuers: 2024 Credit Card Complaints",
        "",
        f"- Complaints analyzed: {summary['complaints_total']:,} across {summary['companies']} companies",
        f"- Capital One complaints: {summary['capone_complaints']:,}",
        "",
        "## 'Card opened without my consent or knowledge'",
        f"- Capital One: {share_cap:.1%} of its complaints",
        f"- Peers: {share_peer:.1%} of their complaints",
        f"- Ratio: {summary['opened_without_consent_ratio']:.2f}x",
        "",
        "## Relief rates by issue",
        f"- Issues compared (Capital One >= {MIN_N} complaints): {summary['issues_compared']}",
        f"- Capital One trails peers on {summary['issues_capone_trails']} of {summary['issues_compared']} issues",
        f"- Extra relieved complaints per year if Capital One matched peer rates: "
        f"{summary['extra_relief_if_matched_peer_rates']:,}",
        f"- Overall relief rate: Capital One {summary['overall_relief_rate_capone']:.1%}, "
        f"peers {summary['overall_relief_rate_peers']:.1%}",
        "",
        "Full table: results/relief_by_issue.csv",
    ]
    (OUT / "results.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

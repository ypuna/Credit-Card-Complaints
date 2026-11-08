# Capital One vs. 10 Peer Card Issuers: 2024 Credit Card Complaints

Compares how Capital One handles 2024 credit card complaints with 10 large peer card issuers, using the public CFPB Consumer Complaint Database.

## Data
- `data/cc2024_capone_vs_10_peers.csv`: 42,363 complaints from 2024 (Capital One plus 10 peers). Built from the full CFPB export with `build_subset.py`.
- Peers: Citibank, Synchrony, JPMorgan Chase, American Express, Bank of America, Bread Financial, Discover, Wells Fargo, Goldman Sachs, Barclays.
- Source: consumerfinance.gov, Consumer Complaint Database.

## Run
```
pip install pandas
python analysis.py                       # uses the included subset
python build_subset.py complaints.csv    # optional: rebuild the subset from the full export
```

## Method
- "Relief" = company response "Closed with monetary relief" or "Closed with non-monetary relief."
- Issues are compared only where Capital One has at least 50 complaints (12 issues).
- Extra relief = for each issue where Capital One trails the peer rate, (peer rate - Capital One rate) x Capital One complaints.

## Key findings
- "Card opened without my consent or knowledge" is 13.6% of Capital One's complaints vs. 6.9% for peers (1.97x).
- Capital One trails peers on relief rates for 11 of 12 issues.
- Overall relief: Capital One 25.7%, peers 36.2%.
- Matching peer relief rates on each issue would yield about 684 more relieved complaints per year.

## Note on the estimate
The "684" figure uses the method above. An earlier draft of this project cited 616. That number does not reproduce from this data.

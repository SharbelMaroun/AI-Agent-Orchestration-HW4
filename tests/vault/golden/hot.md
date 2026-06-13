# Hot

## Top centrality nodes

| Node | Degree | Community |
|---|---|---|
| checkout | 7 | [[payments]] |
| billing | 3 | [[payments]] |
| login | 3 | [[auth]] |
| session | 2 | [[auth]] |
| token | 2 | [[auth]] |
| PRD_payments | 1 | [[payments]] |
| cli_main | 1 | [[payments]] |
| invoice | 1 | [[payments]] |
| policy | 1 | [[auth]] |
| pricing | 1 | [[payments]] |

## Entry points

- PRD_payments -> [[payments]]
- cli_main -> [[payments]]
- test_checkout -> [[payments]]

## Anomalies needing review

| Edge | Relation | Confidence | Source |
|---|---|---|---|
| checkout -> login | uses | 0.6 | src/payments/checkout.py |
| billing -> token | reads | 0.6 | src/payments/billing.py |

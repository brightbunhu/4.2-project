# Step 6 - Feature Selection

Candidates: **24**; dropped constant: []; dropped zero-MI: ['is_urban', 'month_of_year', 'commodity_Beans (sugar)', 'months_since_last_reported_price', 'commodity_Maize meal', 'commodity_Toothpaste'].
Selected: **18** features.

## Mutual-information ranking
```
                             feature  mutual_info  rank
0                        rainfall_1m     0.187353     1
1                  rainfall_6m_total     0.186425     2
2                rainfall_3m_anomaly     0.182751     3
3                  rainfall_3m_total     0.181110     4
4                 rainfall_12m_total     0.177634     5
5                  spi_pct_change_3m     0.105901     6
6                          spi_lag_1     0.095180     7
7                     log_population     0.077322     8
8                          spi_lag_2     0.046767     9
9                               year     0.011873    10
10         commodity_Oil (vegetable)     0.011274    11
11                   commodity_Sugar     0.010524    12
12                    commodity_Rice     0.004620    13
13                   commodity_OTHER     0.004518    14
14                    commodity_Salt     0.003873    15
15            commodity_Laundry soap     0.002334    16
16           commodity_Handwash soap     0.001190    17
17          commodity_Fish (kapenta)     0.000475    18
18                          is_urban     0.000000    19
19                     month_of_year     0.000000    20
20           commodity_Beans (sugar)     0.000000    21
21  months_since_last_reported_price     0.000000    22
22              commodity_Maize meal     0.000000    23
23              commodity_Toothpaste     0.000000    24
```
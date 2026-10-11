# Step 5 - Exploratory Data Analysis

Loaded `commodity_training_table.csv`: **10,418 rows x 47 cols**.

## Target balance
```
              count    pct
price_stress              
0              5456  52.37
1              4962  47.63
```

## Strongest feature correlations with `price_stress`
```
                                  pearson_r
price_spi_raw                        0.3364
spi_pct_dev                          0.3364
spi_lag_1                            0.3214
spi_pct_change_3m                    0.2518
spi_lag_2                            0.2518
price                                0.0840
n_markets                            0.0797
n_price_obs                          0.0797
n_districts_reporting                0.0656
commodity_Laundry soap               0.0109
months_since_last_reported_price     0.0107
commodity_Rice                       0.0100
commodity_Sugar                      0.0096
commodity_Handwash soap              0.0094
commodity_Oil (vegetable)            0.0092
```

## Seasonality (% in stress by calendar month)
```
               stress_pct
month_of_year            
1                    46.5
2                    44.8
3                    46.3
4                    47.9
5                    49.1
6                    50.0
7                    47.7
8                    46.8
9                    49.6
10                   48.1
11                   47.3
12                   46.8
```

## Stress by province (%)
```
                     stress_pct
province_key                   
HARARE                     22.7
MASHONALAND WEST           31.2
MANICALAND                 31.8
MASHONALAND CENTRAL        38.5
MIDLANDS                   42.8
MASHONALAND EAST           42.8
MASVINGO                   56.5
BULAWAYO                   57.7
MATABELELAND SOUTH         67.5
MATABELELAND NORTH         71.8
```
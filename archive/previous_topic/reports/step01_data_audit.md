# Step 1 - Raw Data Audit

## Source overview
| Dataset | Rows | Columns | Duplicate rows |
|---|---|---|---|
| food_price | 25,554 | 22 | 0 |
| poverty | 33 | 14 | 0 |
| rainfall | 5,100 | 20 | 0 |
| population | 5,508 | 17 | 0 |

## Boundary layers
| Level | Features | CRS |
|---|---|---|
| adm1 | 10 | EPSG:4326 |
| adm2 | 91 | EPSG:4326 |

## Missingness (columns with any nulls)
**food_price**: `provider_admin1_name`=214, `provider_admin2_name`=214, `admin1_code`=214, `admin1_name`=214, `admin2_code`=214, `admin2_name`=214, `lat`=214, `lon`=214

**poverty**: `provider_admin1_name`=3, `admin1_code`=3, `admin1_name`=3

**rainfall**: `provider_admin2_name`=5100, `admin2_code`=5100, `admin2_name`=5100, `provider_admin2_code`=5100

**population**: `provider_admin1_name`=54, `provider_admin2_name`=594, `admin1_code`=54, `admin1_name`=54, `admin2_code`=594, `admin2_name`=594, `min_age`=306, `max_age`=612

# Data Dictionary
Unit of analysis: commodity × district × month
Target: price_stress = 1 if SPI > 1.0 else 0
SPI: price / median(price) within same commodity, month, currency
months_since_last_reported_price: calendar month difference to previous observed price for same district-commodity

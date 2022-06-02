from matplotlib.pyplot import table
import requests
from openpyxl import Workbook

# Write the data to an Excel file
listing_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
listings_data = requests.get(listing_url, headers={"X-CMC_PRO_API_KEY": "58160cd4-a7be-414c-8671-7828e8b7a2d9"}).json()['data']
file = Workbook()
sheet = file.create_sheet("Market Listing")
i = 1
sheet.append(['Index','Name', 'Symbol', 'Price', 'Market Cap', 'Volume (24h)', 'Circulating Supply', 'Change (1h)', 'Change (24h)', 'Change (7d)'])
for coin in listings_data:
    sheet.append([i, coin['name'], coin['symbol'], coin['quote']['USD']['price'], coin['quote']['USD']['market_cap'], coin['quote']['USD']['volume_24h'], coin['circulating_supply'], coin['quote']['USD']['percent_change_1h'], coin['quote']['USD']['percent_change_24h'], coin['quote']['USD']['percent_change_7d']])
    i +=1
file.save("CoinMarketCap_MarketListing.xlsx")

print("\n")
print("Market Listing saved to CoinMarketCap_MarketListing.xlsx")

   
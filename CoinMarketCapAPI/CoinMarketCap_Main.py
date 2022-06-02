from matplotlib.pyplot import table
import requests
from prettytable import PrettyTable

listing_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
listings_data = requests.get(listing_url, headers={"X-CMC_PRO_API_KEY": "58160cd4-a7be-414c-8671-7828e8b7a2d9"}).json()['data']

coins = []
def get_market_listing() -> table:
    """
    Returns data around the cryptocurrency market
    """
    table = PrettyTable(['Name', 'Symbol', 'Price', 'Market Cap', 'Volume (24h)', 'Circulating Supply', 'Change (1h)', 'Change (24h)', 'Change (7d)'])
    for coin in listings_data:
        coins.append([coin['name'], coin['symbol'], coin['quote']['USD']['price'], coin['quote']['USD']['market_cap'], coin['quote']['USD']['volume_24h'], coin['circulating_supply'], coin['quote']['USD']['percent_change_1h'], coin['quote']['USD']['percent_change_24h'], coin['quote']['USD']['percent_change_7d']])
    
    # Sort the coins by the user selected option
    while True:
        print("Press..")
        number = 1
        # Display the choices to the user
        for item in table.field_names:
            print(str(number) + ": " + item)
            number +=1
        choice = int(input("Choose the number you want to sort: "))

        # Sort the coins by the user selected option
        coins.sort(key = lambda x: x[int(choice)- 1] , reverse=True)

        # Add the sorted coins list to the table and print it
        for coin in coins[:100]:
            table.add_row(coin)
        print(table)
        table.clear_rows()
        print("\n")

        #Quit the program
        choice = input("Press 'q' to quit or any other key to continue: ")
        if choice == 'q':
            break

   

print(get_market_listing(), sep = "\n")



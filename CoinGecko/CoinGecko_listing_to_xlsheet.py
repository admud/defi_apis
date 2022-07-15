from matplotlib.pyplot import table
import requests
from openpyxl import Workbook
import pandas as pd
import pickle
import os
from googleapiclient.discovery import build
from mimetypes import MimeTypes
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload



class RestConnection:
    global SCOPES
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self,apikey):
        self.apikey = apikey
        self.listing_url = "https://pro-api.coingecko.com/api/v3"
        self.headers = {"content-type": "application/json"}
        self.parameters = {"x_cg_pro_api_key" : apikey}
        

        path = os.path.expanduser("~/m3_google_pickle_write")
        with open(path, "rb") as token:
            self.creds = pickle.load(token)

        # Connect to the API service
        self.service = build("drive", "v3", credentials=self.creds)

    def FileUpload(self, filepath: str, folderid: str) -> None:
        name = filepath.split("/")[-1]

        mimetype = MimeTypes().guess_type(name)[0]

        file_metadata = {"name": name, "parents": [folderid]}
        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)

            file = (
                self.service.files()
                .create(
                    body=file_metadata,
                    media_body=media,
                    fields="id",
                )
                .execute()
            )

            print(f"{filepath} Uploaded.")

        except Exception as e:
            print(e)

            raise Exception("Can't Upload File.")

    
    # Get market listing from CoinGecko . Default - 250 a page
    def get_market_listing(self,page):
        endpoint = "/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=250&page=" + str(page) + "&sparkline=false"
        response = requests.get(self.listing_url + endpoint, headers = self.headers, params = self.parameters).json()
        listingdf = pd.DataFrame(response)
        listingData = listingdf.iloc[0:251,[0,1,2,4,25]]
        return listingData

    # Concatinate the excel sheets into one big Data Frame
    def concatinate_dfs(self,workbook_url):
        all_dfs = pd.read_excel(workbook_url, sheet_name=None)
        dfs = pd.concat(all_dfs, ignore_index=True)
        return dfs

    # Get market listing for a manual coin other than the one in 2500 listings
    def get_market_listing_for_manual_coins(self,coin):
        endpoint = "/coins/markets?vs_currency=usd&ids=" + str(coin) + "&order=market_cap_desc&per_page=100&page=1&sparkline=false"
        response = requests.get(self.listing_url + endpoint, headers = self.headers, params = self.parameters).json()
        return response



# Driver Code
marketData = RestConnection("CG-HtMzQmUGssCJkBeMEz7n6Q4Y")

# ### Upload to GSheet
PRICING_FOLDER = "1vKDKMs6Hj9ADsJyaEP9VyHYo0YQzXCDw"

### Get market listing for Top 2500 coins from Coin Gecko

j = 1
with pd.ExcelWriter('CoinGecko_MarketListing.xlsx') as writer:
    for i in range(1,11):
        df = marketData.get_market_listing(i)
        df.to_excel(writer, sheet_name='Sheet' + str(j), index=False)
        print("sheet " + str(j) + " saved")
        j +=1
workbook_url = r"C:\Users\deepa\OneDrive\Documents\GitHub\defi_apis\CoinGecko_MarketListing.xlsx"
all_dfs = marketData.concatinate_dfs(workbook_url)
all_dfs.to_excel("CoinGecko_2500_MarketListing_summary.xlsx", index=False)
print('DataFrame is written to Excel File successfully.')
marketData.FileUpload(r"C:\Users\deepa\OneDrive\Documents\GitHub\defi_apis\CoinGecko_2500_MarketListing_summary.xlsx", PRICING_FOLDER)
### Get market listing for manual coins and store them in the excel file

manual_coins = pd.read_csv(r"C:\Users\deepa\OneDrive\Documents\GitHub\defi_apis\CoinGecko_MarketListing_Manual_coins - Manual.csv")
manual_coin_names = manual_coins.iloc[:,2]
manual_coin_names = manual_coin_names.values.tolist()
frames = []
for name in manual_coin_names:
    frames += marketData.get_market_listing_for_manual_coins(name)
listingdf = pd.DataFrame(frames)
print(listingdf.info())
print("\n")
listingData = listingdf.iloc[0:251,[0,1,2,25,4]]
print(listingData)
writer = pd.ExcelWriter('CoinGecko_MarketListing - Manual.xlsx')
# write dataframe to excel
listingData.to_excel(writer,index = False)
# save the excel
writer.save()
print('The Manual unrated coins Market Listing DataFrame is written to Excel File successfully.')
  




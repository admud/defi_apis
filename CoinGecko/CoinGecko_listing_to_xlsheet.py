from matplotlib.pyplot import table
import requests
from openpyxl import Workbook
import pandas as pd
import pickle
import os
from googleapiclient.discovery import build
from mimetypes import MimeTypes
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from apiclient import errors
from google_drive_downloader import GoogleDriveDownloader as gdd
from pprint import pprint
import SendEmail
import GUpload
import time


class RestConnection:
    global SCOPES
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self,apikey):
        self.apikey = apikey
        self.listing_url = "https://pro-api.coingecko.com/api/v3"
        self.headers = {"content-type": "application/json"}
        self.parameters = {"x_cg_pro_api_key" : apikey}

    
    # Get market listing from CoinGecko . Default - 250 a page
    def get_market_listing(self,page):
        endpoint = f"/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=250&page={str(page)}&sparkline=false"

        response = requests.get(self.listing_url + endpoint, headers = self.headers, params = self.parameters).json()
        #listingdf = pd.DataFrame(response)
        return response

    # Concatinate the excel sheets into one big Data Frame
    def concatinate_dfs(self,workbook_url):
        all_dfs = pd.read_excel(workbook_url, sheet_name=None)
        return pd.concat(all_dfs, ignore_index=True)

    # Get market listing for a manual coin other than the one in 2500 listings
    def get_market_listing_for_manual_coins(self,coin):
        endpoint = f"/coins/markets?vs_currency=usd&ids={str(coin)}&order=market_cap_desc&per_page=100&page=1&sparkline=false"

        return requests.get(self.listing_url + endpoint, headers=self.headers, params=self.parameters).json()

def main():
    # Driver Code
    marketData = RestConnection("CG-HtMzQmUGssCJkBeMEz7n6Q4Y")

    # G Sheet Folder ID
    PRICING_FOLDER = "1vKDKMs6Hj9ADsJyaEP9VyHYo0YQzXCDw"

    ### Get market listing for Top 2500 coins from Coin Gecko
    
    start_time = time.time()
    df = []
    with pd.ExcelWriter('CoinGecko_MarketListing.xlsx') as writer:
        for i in range(1,11):
            df += marketData.get_market_listing(i)

        df = pd.DataFrame(df)
        df = df.iloc[:,[0,1,2,4,25]]
        df.to_excel(writer, sheet_name="Top 2500", index=False)
        print('DataFrame is written to Excel File successfully.')

    # #### Upload the excel sheet to Google Drive ####
    # GUpload.marketData.GoogleFileUpload("CoinGeckoPrices.xlsx", PRICING_FOLDER)

    # ### Get market listing for manual coins and store them in the excel file

    manual_coins = pd.read_csv(r"C:\Users\deepa\OneDrive\Documents\GitHub\defi_apis\CoinGecko_MarketListing_Manual_coins - Manual.csv")
    manual_coin_names = manual_coins.iloc[:,2]
    manual_coin_names = manual_coin_names.values.tolist()
    frames = []
    for name in manual_coin_names:
        frames += marketData.get_market_listing_for_manual_coins(name)
    listingdf = pd.DataFrame(frames)
    listingdf = listingdf.iloc[0:251,[0,1,2,4,25]]

    writer = pd.ExcelWriter('CoinGecko_manualcoins.xlsx')
    # write dataframe to excel
    listingdf.to_excel(writer,sheet_name = 'Unranked Coins',index = False)
    # save the excel
    writer.save()
    print('The Manual unrated coins Market Listing DataFrame is written to Excel File successfully.')
    

    # Read excel file
    # and store into a DataFrame
    df1 = pd.read_excel('CoinGecko_MarketListing.xlsx')
    df2 = pd.read_excel('CoinGecko_manualcoins.xlsx')
    
    # concat both DataFrame into a single DataFrame
    df = pd.concat([df1, df2])
    
    # Export Dataframe into Excel file
    df.to_excel('CG_summary.xlsx', index=False)

    ### Send Email with the excel file as an attachment
    recipients = "deepa@jstdigitaltrading.com"
    SendEmail.send_notification_email_with_file(recipients, "CoinGecko Prices for Top 2500 + Unranked coins", "CoinGecko_Summary_MarketListing", r"C:\Users\deepa\OneDrive\Documents\GitHub\defi_apis\CG_summary.xlsx")
   
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Execution time:', elapsed_time, 'seconds')
if __name__ == "__main__":
    main()



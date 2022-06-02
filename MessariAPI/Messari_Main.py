# from six.moves import urllib
# url = "https://data.messari.io/api/v2/assets"
# print(urllib.request.urlopen(url).read())
import pandas as pd
from messari.messari import Messari

# Provide the Messari API key
messari = Messari('5306d020-6156-40e9-8fb5-6909fe0b2559')

# Get the list of all assets
def GetAssets():
    response_data_df = messari.get_all_assets(asset_fields=['metrics'], to_dataframe=True)
    return response_data_df

# Get Metrics for all the available assets
def GetMetrics():
    dfs = []
    for i in range(1,5,1):
        response_data_df = messari.get_all_assets(asset_fields=['metrics'], to_dataframe=True)
        dfs.append(response_data_df)
    return pd.concat(dfs).head


print(GetAssets())
print(GetMetrics())
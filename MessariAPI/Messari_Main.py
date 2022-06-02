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

# Get metrics for a given set of assests for a given date range
def GetMetricsForAssets(asset_ids, start_date, end_date):
    metric = 'price'
    timeseries_df = messari.get_metric_timeseries(asset_slugs=asset_ids, asset_metric=metric, start=start_date, end=end_date, to_dataframe=True)
    return timeseries_df

# Get the list of all exchanges and pairs
def GetExchanges():
    exchanges_df = messari.get_all_markets(to_dataframe=True)
    return exchanges_df

# print(GetAssets())
# print(GetMetrics())
print(GetMetricsForAssets(['btc', 'eth'], '2019-01-01', '2019-12-31'))
#print(GetExchanges())
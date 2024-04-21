import requests

# https://www.alphavantage.co/documentation/
url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo'
# r = requests.get(url)
# data = r.json()
# print(data)

def download_csv_from_github(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"CSV file downloaded to {save_path}.")

# https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
# https://github.com/turingplanet/web-data-extraction-intro
url = "https://raw.githubusercontent.com/turingplanet/web-data-extraction-intro/main/sample_stock_data.csv"
save_path = "github_csv_file.csv"
download_csv_from_github(url, save_path)

import requests

def fetch_data_from_source2():
    url = "http://source2/api/stations"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
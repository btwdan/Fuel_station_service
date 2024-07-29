import requests

def fetch_data_from_source1():
    url = "http://source1/api/stations"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
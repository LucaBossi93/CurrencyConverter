import xmltodict
import requests
import json
import pandas as pd

URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"

payload = {}
headers = {}

response = requests.request("GET", URL, headers=headers, data=payload)

response_encoded = response.text.encode('utf8')

# Converts the xml file obtained from the website into a dictionary
doc = xmltodict.parse(response_encoded)

with open('data.json', 'w') as fp:
    json.dump(doc, fp, sort_keys=True, indent=4)

# From the source dictionary, another dictionary is created containing only the data useful for the application.
cur_list = doc["gesmes:Envelope"]["Cube"]["Cube"]

new_dict = {}

for day in cur_list:
    new_dict[day["@time"]] = {}
    new_dict[day["@time"]]["EUR"] = float(1)
    for row in day["Cube"]:
        new_dict[day["@time"]][row["@currency"]] = float(row["@rate"])

# A dataframe is created using pandas
dfcur = pd.DataFrame.from_dict(new_dict)
import xmltodict
import requests
import json

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

days_cur = {}

for day in cur_list:
    days_cur[day["@time"]] = {}
    days_cur[day["@time"]]["EUR"] = float(1)
    for row in day["Cube"]:
        days_cur[day["@time"]][row["@currency"]] = float(row["@rate"])

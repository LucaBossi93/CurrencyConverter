import requests
import pandas as pd
import json
import xmltodict
import numpy as np
from datetime import datetime
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

response_encoded = response.text.encode('utf8')

doc = xmltodict.parse(response_encoded)

with open('data.json', 'w') as fp:
    json.dump(doc, fp, sort_keys=True, indent=4)
lista = doc["gesmes:Envelope"]["Cube"]["Cube"]
new_dict = {}

for day in lista:
    new_dict[day["@time"]] = {}
    new_dict[day["@time"]]["EUR"] = float(1)
    for row in day["Cube"]:
        new_dict[day["@time"]][row["@currency"]] = float(row["@rate"])

dfcur = pd.DataFrame.from_dict(new_dict)

datetime_object = datetime.strptime('2014-02-20', '%Y-%m-%d')
print(datetime_object)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/converter", methods=['GET'])
def get_input():
    amount = (request.args.get("amount"))
    src_currency = (request.args.get("src_currency"))
    dest_currency = request.args.get("dest_currency")
    reference_date = request.args.get("reference_date")

    try:
        amount, src_currency, dest_currency, reference_date = _validate_inputs(amount, src_currency, dest_currency,
                                                                               reference_date)
    except AttributeError as e:
        return str(e)
    except ValueError as e:
        return str(e)
    except KeyError as e:
        return str(e)

    converted_value = _convert_currency(amount, src_currency, dest_currency, reference_date)
    return '''<h1>The language value is: {}</h1>'''.format(converted_value)


def _validate_inputs(amount, src_currency, dest_currency, reference_date):
    return _validate_amount(amount), _validate_src_currency(src_currency), _validate_dest_currency(
        dest_currency), _validate_reference_date(reference_date)


def _validate_src_currency(src_currency):
    try:
        src_currency = src_currency.upper()
    except AttributeError:
        raise AttributeError("")
    try:
        if dfcur.loc[src_currency].any():
            return src_currency
    except KeyError:
        raise KeyError("{} doesn't exist".format(src_currency)) from KeyError


def _validate_dest_currency(dest_currency):
    try:
        dest_currency = dest_currency.upper()
    except AttributeError:
        raise
    try:
        if dfcur.loc[dest_currency].any():
            return dest_currency
    except KeyError:
        raise KeyError("{} doesn't exist".format(dest_currency)) from KeyError


def _validate_amount(amount):
    try:
        return np.float(amount)
    except ValueError:
        raise ValueError("{} is not valid".format(amount))


def _validate_reference_date(reference_date):
    try:
        if dfcur[reference_date].any():
            return reference_date
    except KeyError:
        raise KeyError("{} doesn't exist".format(reference_date)) from KeyError


def _convert_currency(amount, src_currency, dest_currency, reference_date):
    currencies_rates = dfcur[reference_date]
    print(currencies_rates)
    src_value = currencies_rates[src_currency]
    print(src_value)
    dest_value = currencies_rates[dest_currency]
    print(dest_value)
    print(np.divide(np.multiply(np.float(amount), dest_value), src_value))
    return np.divide(np.multiply(np.float(amount), dest_value), src_value)


if __name__ == "__main__":
    app.run()

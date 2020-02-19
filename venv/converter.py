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

# a dataframe is created using pandas
dfcur = pd.DataFrame.from_dict(new_dict)


@app.route("/")
def homes():
    return "This Application allows you to convert currencies."


@app.route("/converter", methods=['GET'])
def get_input():
    """
    Function that receives data via GET, validates it and performs currency conversion.

    :return: the converted currency is returned as json
    """
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
    return jsonify(amount=converted_value, currency=dest_currency)


def _validate_inputs(amount, src_currency, dest_currency, reference_date):
    """
    Function that recalls the various input validation methods

    :param amount: Amount of currency you want to convert
    :param src_currency: Source currency code received as input.
    :param dest_currency: Destination currency code
    :param reference_date: Date on which the operation is executed
    :return: Return validated inputs
    """
    return _validate_amount(amount), _validate_src_currency(src_currency), _validate_dest_currency(
        dest_currency), _validate_reference_date(reference_date)


def _validate_src_currency(src_currency):
    """
    Function that checks that the source currency code as input is correct.
    If the value is invalid it generates an error, otherwise it returns the value it received as converted input.

    :param src_currency: Source currency code received as input.
    :return: Validated source currency code
    """
    try:
        src_currency = src_currency.upper()
    except AttributeError:
        raise AttributeError("src_currency code is not valid") from AttributeError
    try:
        if dfcur.loc[src_currency].any():
            return src_currency
    except KeyError:
        raise KeyError("{} doesn't exist".format(src_currency)) from KeyError


def _validate_dest_currency(dest_currency):
    """
    Function that checks that the destination currency code as input is correct.
    If the value is invalid it generates an error, otherwise it returns the value it received as converted input.

    :param dest_currency: Destination currency code received as input.
    :return: Validated destination currency code
    """
    try:
        dest_currency = dest_currency.upper()
    except AttributeError:
        raise AttributeError("src_currency code is not valid") from AttributeError
    try:
        if dfcur.loc[dest_currency].any():
            return dest_currency
    except KeyError:
        raise KeyError("{} doesn't exist".format(dest_currency)) from KeyError


def _validate_amount(amount):
    """
    Function that checks that the amount to be converted received as input is valid

    :param amount: Amount of currency you want to convert
    :return:  Validated amount
    """
    try:
        return np.float(amount)
    except ValueError:
        raise ValueError("{} is not valid".format(amount))


def _validate_reference_date(reference_date):
    """
    Function that checks that the reference date entered by the user is valid

    :param reference_date: reference date received as input
    :return: Validated reference date
    """
    try:
        if dfcur[reference_date].any():
            return reference_date
    except KeyError:
        raise KeyError("{} doesn't exist".format(reference_date)) from KeyError


def _convert_currency(amount, src_currency, dest_currency, reference_date):
    """
    Function that performs currency conversion from previously validated data.

    :param amount: Validated amount of currency you want to convert
    :param src_currency: Validated source currency code.
    :param dest_currency: Validated destination currency code
    :param reference_date: Validated date on which the operation is executed .
    :return:
    """
    currencies_rates = dfcur[reference_date]
    src_value = currencies_rates[src_currency]
    dest_value = currencies_rates[dest_currency]
    return np.divide(np.multiply(np.float(amount), dest_value), src_value)


if __name__ == "__main__":
    app.run()

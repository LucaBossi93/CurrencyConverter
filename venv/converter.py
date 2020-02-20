import numpy as np
from datetime import datetime
from flask import Flask
from flask import jsonify
from flask import request
import bootstrap

app = Flask(__name__)

days_cur = bootstrap.days_cur


@app.route("/")
def homes():
    return "This Application allows you to convert currencies."


@app.route("/converter", methods=['GET'])
def get_input():
    """
    Receives data via GET, validates it and performs currency conversion.

    :return: the converted currency is returned as json
    """
    amount = (request.args.get("amount"))
    src_currency = (request.args.get("src_currency"))
    dest_currency = request.args.get("dest_currency")
    reference_date = request.args.get("reference_date")

    try:
        amount, src_currency, dest_currency, reference_date = _convert_inputs(amount, src_currency, dest_currency,
                                                                              reference_date)
    except (AttributeError, ValueError, KeyError) as e:
        return str(e)

    converted_value = _convert_currency(amount, src_currency, dest_currency, reference_date)
    return jsonify(amount=converted_value, currency=dest_currency)


def _convert_inputs(amount, src_currency, dest_currency, reference_date):
    """
    Recalls the various input validation methods

    :param amount: Amount of currency you want to convert.
    :param src_currency: Source currency code received as input.
    :param dest_currency: Destination currency code.
    :param reference_date: Date on which the operation is executed.
    :return: Validated inputs.
    """
    return _convert_amount(amount), _convert_src_currency(src_currency), _convert_dest_currency(
        dest_currency), _validate_reference_date(reference_date)


def _convert_src_currency(src_currency):
    """
    Checks that the source currency code as input is correct.
    If the value is invalid it generates an error, otherwise it returns the value it received as converted input.

    :param src_currency: Source currency code received as input.
    :return: Validated source currency code.
    """
    try:
        src_currency = src_currency.upper()
    except AttributeError:
        raise AttributeError("src_currency code is not valid") from AttributeError

    fist_day = list(days_cur.keys())[0]
    if src_currency in days_cur[fist_day]:
        return src_currency
    else:
        raise KeyError("{} doesn't exist".format(src_currency))


def _convert_dest_currency(dest_currency):
    """
    Checks that the destination currency code as input is correct.
    If the value is invalid it generates an error, otherwise it returns the value it received as converted input.

    :param dest_currency: Destination currency code received as input.
    :return: Validated destination currency code.
    """
    try:
        dest_currency = dest_currency.upper()
    except AttributeError:
        raise AttributeError("src_currency code is not valid") from AttributeError

    fist_day = list(days_cur.keys())[0]
    if dest_currency in days_cur[fist_day]:
        return dest_currency
    else:
        raise KeyError("{} doesn't exist".format(dest_currency))


def _convert_amount(amount):
    """
    Checks that the amount to be converted received as input is valid

    :param amount: Amount of currency you want to convert.
    :return:  Validated amount.
    """
    try:
        return np.float(amount)
    except ValueError:
        raise ValueError("{} is not valid".format(amount))


def _validate_reference_date(reference_date):
    """
    Checks that the reference date entered by the user is valid

    :param reference_date: Reference date received as input.
    :return: Validated reference date.
    """
    try:
        if days_cur[reference_date]:
            return reference_date
    except KeyError:
        raise KeyError("{} doesn't exist".format(reference_date)) from KeyError


def _convert_currency(amount, src_currency, dest_currency, reference_date):
    """
    Performs currency conversion from previously validated data.

    :param amount: Validated amount of currency you want to convert.
    :param src_currency: Validated source currency code.
    :param dest_currency: Validated destination currency code.
    :param reference_date: Validated date on which the operation is executed.
    :return: The converted value.
    """
    currencies_rates = days_cur[reference_date]
    src_value = currencies_rates[src_currency]
    dest_value = currencies_rates[dest_currency]
    return np.divide(np.multiply(np.float(amount), dest_value), src_value)


if __name__ == "__main__":
    app.run()

import converter as c
import pytest


def test_date_validation():
    date = list(c.dfcur)[0]
    assert c._validate_reference_date(date) == date

    with pytest.raises(KeyError):
        c._validate_reference_date("2020--10") == "2020-02-10"
    with pytest.raises(KeyError):
        c._validate_reference_date("2020-2-1") == "2020-02-01"


def test_dest_currency_validation():
    assert c._validate_dest_currency("EUR") == "EUR"

    assert c._validate_dest_currency("eur") == "EUR"

    assert c._validate_dest_currency("Usd") == "USD"

    with pytest.raises(KeyError):
        c._validate_dest_currency("#54fdc")

    with pytest.raises(AttributeError):
        c._validate_dest_currency(None)


def test_src_currency_validation():
    assert c._validate_src_currency("EUR") == "EUR"

    assert c._validate_src_currency("eur") == "EUR"

    assert c._validate_src_currency("Usd") == "USD"

    with pytest.raises(KeyError):
        c._validate_src_currency("#54fdc")

    with pytest.raises(AttributeError):
        c._validate_src_currency(None)


def test_amount_validation():
    assert c._validate_amount(12) == 12
    assert c._validate_amount(100.33) == 100.33

    with pytest.raises(ValueError):
        c._validate_amount("15,1")

    with pytest.raises(ValueError):
        c._validate_amount("abc")

    with pytest.raises(ValueError):
        c._validate_amount("15'1")

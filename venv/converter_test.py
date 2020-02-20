import converter as c
import pytest

def test_date_validation():
    date = list(c.dfcur)[0]
    assert c._validate_reference_date(date) == date


@pytest.mark.parametrize("test_input", ["2019-10-02", "2019-0-02", "2020--2", "a", 15])
def test_date_validation_exception(test_input):
    with pytest.raises(KeyError):
        c._validate_reference_date(test_input)


@pytest.mark.parametrize("test_input, excepted", [("Eur", "EUR"), ("eur", "EUR"), ("USD", "USD"), ("BGn", "BGN")])
def test_dest_currency_conversion(test_input, excepted):
    assert c._convert_dest_currency(test_input) == excepted


@pytest.mark.parametrize("test_input", ["EU", "èur", "BNG"])
def test_dest_currency_conversion_exception(test_input):
    with pytest.raises(KeyError):
        c._convert_dest_currency(test_input)

    with pytest.raises(AttributeError):
        c._convert_dest_currency(None)

    with pytest.raises(AttributeError):
        c._convert_dest_currency(12)


@pytest.mark.parametrize("test_input, excepted", [("Eur", "EUR"), ("eur", "EUR"), ("USD", "USD"), ("BGn", "BGN")])
def test_src_currency_conversion(test_input, excepted):
    assert c._convert_src_currency(test_input) == excepted


@pytest.mark.parametrize("test_input", ["EU", "èur", "BNG"])
def test_src_currency_conversion_exception(test_input):
    with pytest.raises(KeyError):
        c._convert_src_currency(test_input)

    with pytest.raises(AttributeError):
        c._convert_src_currency(None)

    with pytest.raises(AttributeError):
        c._convert_src_currency(14)


@pytest.mark.parametrize("test_input, excepted", [(12, 12), (12.34, 12.34), (12.0, 12), (0.0, 0.0)])
def test_amount_conversion(test_input, excepted):
    assert c._convert_amount(test_input) == excepted


@pytest.mark.parametrize("test_input", ["15,1", "abc", "15'1"])
def test_amount_conversion_exception(test_input):
    with pytest.raises(ValueError):
        c._convert_amount(test_input)

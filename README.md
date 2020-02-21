# Currency Converter

API to calculate the conversion between some currencies including EUR, USD, GBP, ... according to exchange rates updated to the last 90 working days that can be found on the [European Bank's website](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml).

## Installation

Download or clone the repository to a local folder. To execute the flask application run

```bash
python3 converter.py   
```
## Dependencies
The requirements.txt file contains all the dependencies necessary for the proper functioning of the application


## Usage
Once the application is running in localhost, one can send a GET request to the API at endpoint "converter" as the following example:
```bash
curl --location --request GET 'http://127.0.0.1:5000/converter?amount=100&src_currency=USD&dest_currency=EUR&reference_date=2020-02-20'
```
where __amount__ is the value to be converted, __src_currency__ is the ISO currency code for the source currency to convert (e.g. EUR,
USD, GBP), __dest_currency__ is the  ISO currency code for the destination currency to convert (e.g. EUR,
USD, GBP), and __reference_date__ is the reference date for the exchange rate, in YYYY-MM-DD format.

The API returns a JSON of type:

```json
{"amount":92.67840593141798,"currency":"EUR"}
```

Where __amount__ and __currency__ are the corresponding converted amount and the ISO code of the destination currency.

If the currency ISO code is not recognised or present on the [European Bank's website](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml) or the reference date is not listed on the website, a string error is returned.

## Docker installation
To create a docker image of the application, simply run the following command:
```bash
docker build --tag converter .
```
This command builds a docker image from the DockerFile in the project folder.

Once the image is created, use the following command to run the application:

```bash
docker run --name python-app-converter -p 5000:5000 converter
```
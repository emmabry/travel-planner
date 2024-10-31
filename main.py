import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = 'https://test.api.amadeus.com/'
FIND_FLIGHTS = 'v2/shopping/flight-offers'
FLIGHT_PRICE = 'v1/shopping/flight-offers/pricing'


def get_token():
    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    api_key = os.getenv('API_KEY_AMADEUS')
    api_secret = os.getenv('API_SECRET_AMADEUS')
    header = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    params = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': api_secret,
    }
    response = requests.post(auth_url, data=params, headers=header)
    token = response.json()['access_token']
    return token


def check_flights():
    header = {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
    }
    params = {
        'originLocationCode': 'LHR',
        'destinationLocationCode': 'CDG',
        'departureDate': '2024-12-10',
        'returnDate': '2024-12-15',
        'adults': 1,
        'nonStop': 'true'

    }
    response = requests.get(BASE_URL + FIND_FLIGHTS, headers=header, params=params)
    offers = response.json()
    print(offers)
    first_offer = offers['data'][0]
    return first_offer


def get_price(first_offer):
    header = {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json',
        'X-HTTP-Method-Override': 'GET'
    }
    body = {
        "data": {
            "type": "flight-offers-pricing",
            "flightOffers": [first_offer]
        }
    }
    response = requests.post(BASE_URL + FLIGHT_PRICE, headers=header, json=body)
    price_details = response.json()
    return price_details


def format_offer(price_details):
    pass


if __name__ == '__main__':
    auth_token = get_token()
    first_offer = check_flights()
    price = get_price(first_offer)

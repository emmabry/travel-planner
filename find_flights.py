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


# very clunky inefficient code but using for the time being to check format
def format_offer(price_details):
    print("Here are the details for the found flight:")
    # DETAILS FOR DEPARTING FLIGHT
    departing_shortcut = price_details['data']['flightOffers'][0]['itineraries'][0]["segments"][0]
    duration = departing_shortcut["duration"]
    print(f"The departing flight duration is {duration}")
    departure_iata = departing_shortcut['departure']['iataCode']
    terminal = departing_shortcut['departure']['terminal']
    departure_time = departing_shortcut['departure']['at']
    print(f"The flight departs from {departure_iata} terminal {terminal} at {departure_time}")
    arrival_iata = departing_shortcut['arrival']['iataCode']
    terminal = departing_shortcut['arrival']['terminal']
    arrival_time = departing_shortcut['arrival']['at']
    print(f"The flight arrives at {arrival_iata} terminal {terminal} at {arrival_time}")

    # DETAILS FOR RETURNING FLIGHT
    returning_shortcut = price_details['data']['flightOffers'][0]['itineraries'][1]["segments"][0]
    return_duration = returning_shortcut["duration"]
    print(f"The returning flight duration is {return_duration}")
    returning_iata = returning_shortcut['departure']['iataCode']
    return_terminal = returning_shortcut['departure']['terminal']
    return_time = returning_shortcut['departure']['at']
    print(f'The flight departs from {returning_iata} terminal {return_terminal} at {return_time}')
    r_arrival_iata = returning_shortcut['arrival']['iataCode']
    r_terminal = returning_shortcut['arrival']['terminal']
    r_arrival_time = returning_shortcut['arrival']['at']
    print(f"The flight arrives at {r_arrival_iata} terminal {r_terminal} at {r_arrival_time}")

    # Price Info
    price_shortcut = price_details['data']['flightOffers'][0]['price']
    print(f"The flight price is {price_shortcut['grandTotal']} {price_shortcut['billingCurrency']}")


if __name__ == '__main__':
    auth_token = get_token()
    first_offer = check_flights()
    price = get_price(first_offer)
    format_offer(price)

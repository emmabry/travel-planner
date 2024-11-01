from find_flights import get_token, BASE_URL
import requests

SEARCH_HOTELS = "v1/reference-data/locations/hotels/by-city"
GET_HOTEL_PRICES = "v3/shopping/hotel-offers"


def check_hotels():
    header = {
        'Authorization': 'Bearer ' + get_token(),
        'Content-Type': 'application/json'
    }
    params = {
        'cityCode': 'PAR',
        'radius': '2',
        'ratings': ['4', '5']
    }
    response = requests.get(BASE_URL + SEARCH_HOTELS, headers=header, params=params)
    all_hotels = response.json()
    short_hotel_list = all_hotels['data'][:50]
    hotel_ids = [hotel['hotelId'] for hotel in short_hotel_list]
    return hotel_ids


def get_hotel_prices(hotel_ids):
    header = {
        'Authorization': 'Bearer ' + get_token(),
        'Content-Type': 'application/json'
    }
    params = {
        'hotelIds': hotel_ids,
        'adults': 1,
        'roomQuantity': 1,
        'checkInDate': '2025-04-10',
        'checkOutDate': '2025-04-15'
    }
    response = requests.get(BASE_URL + GET_HOTEL_PRICES, headers=header, params=params)
    hotel_prices = response.json()
    print(hotel_prices)


if __name__ == '__main__':
    get_token()
    get_hotel_prices(check_hotels())

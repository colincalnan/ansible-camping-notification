"""
@see https://github.com/hugsy/stuff/blob/ad6a345ab9e739d76cf5e6be3c0690ce23a298f1/bc_camping.py
"""

import requests
import datetime
import pprint
import json
import sys

"""
curl "https://bccrdr.usedirect.com/rdr/rdr/search/place" ^
  -H "authority: bccrdr.usedirect.com" ^
  -H "accept: application/json, text/javascript, */*; q=0.01" ^
  -H "dnt: 1" ^
  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37" ^
  -H "content-type: application/json" ^
  -H "origin: https://discovercamping.ca" ^
  -H "sec-fetch-site: cross-site" ^
  -H "sec-fetch-mode: cors" ^
  -H "sec-fetch-dest: empty" ^
  -H "referer: https://discovercamping.ca/BCCWeb/Facilities/SearchViewUnitAvailabity.aspx" ^
  -H "accept-language: en-US,en;q=0.9,fr;q=0.8" ^
  --data-binary "^{^\^"PlaceId^\^":^\^"104^\^",^\^"Latitude^\^":0,^\^"Longitude^\^":0,^\^"HighlightedPlaceId^\^":^\^"104^\^",^\^"StartDate^\^":^\^"7-26-2020^\^",^\^"Nights^\^":^\^"2^\^",^\^"CountNearby^\^":true,^\^"NearbyLimit^\^":100,^\^"NearbyOnlyAvailable^\^":true,^\^"NearbyCountLimit^\^":10,^\^"Sort^\^":^\^"Distance^\^",^\^"CustomerId^\^":^\^"0^\^",^\^"RefreshFavourites^\^":true,^\^"IsADA^\^":false,^\^"UnitCategoryId^\^":^\^"2^\^",^\^"SleepingUnitId^\^":^\^"10^\^",^\^"MinVehicleLength^\^":0,^\^"UnitTypesGroupIds^\^":^[^]^}" ^
  --compressed
"""

MAX_LOCATION_ID = 160

def get_data(location_id: int, start_date: datetime.datetime, number_of_nights: int) -> requests.Response:
    url = "https://bccrdr.usedirect.com/rdr/rdr/search/place"
    data = {
        "CountNearby": True,
        "CustomerId": "0",
        "HighlightedPlaceId": 0,
        "IsADA": False,
        "Latitude": 0,
        "Longitude": 0,
        "MinVehicleLength": "10",
        "NearbyCountLimit": 1,
        "NearbyLimit": 1,
        "NearbyOnlyAvailable": False,
        "Nights": number_of_nights,
        "PlaceId": location_id,
        "RefreshFavourites": True,
        "SleepingUnitId": "11",
        "Sort": "Distance",
        "StartDate": start_date.strftime("%m-%d-%Y"),
        "UnitCategoryId": "2",
        "UnitTypesGroupIds": []

        # "PlaceId": location_id,
        # "Latitude": 0,
        # "Longitude": 0,
        # "HighlightedPlaceId": location_id,
        # "StartDate": start_date.strftime("%m-%d-%Y"),
        # "Nights": number_of_nights,
        # "CountNearby": False,
        # "NearbyLimit": 0,
        # "NearbyOnlyAvailable": False,
        # "NearbyCountLimit": 0,
        # "Sort": 'Distance',
        # "CustomerId": 0,
        # "RefreshFavourites": True,
        # "IsADA": False,
        # "UnitCategoryId": 2,
        # "SleepingUnitId": 10,
        # "MinVehicleLength": 0,
        # "UnitTypesGroupIds": [],
    }
    h = requests.post(
        url,
        json=data,
        headers={
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
        }
    )

    if h.status_code != requests.codes.ok:
        raise RuntimeError(f"Unexpected code HTTP/{h.status_code}")

    js = h.json()
    if js is None:
        return None

    if js['SelectedPlaceId'] == 0:
        raise KeyError('invalid location_id')

    return js


def print_availability_for_location_and_dates(location_id: int, start_date: datetime.datetime, number_of_nights: int) -> None:
    try:
        js = get_data(location_id, start_date, number_of_nights)
    except KeyError:
        print(f"Error for location id '{location_id}'")
    # pprint.pprint(js)
    if js['SelectedPlace']['Available']:
        for facility_index in js['SelectedPlace']['Facilities']:
            facility = js['SelectedPlace']['Facilities'][facility_index]
            if facility['Available']:
                for unit_type_index in facility['UnitTypes']:
                    unit_type = facility['UnitTypes'][unit_type_index]
                    if unit_type['Available'] and not  unit_type['AvailableFiltered'] and unit_type['AvailableCount'] > 0:
                        print(f"{unit_type['AvailableCount']:d} '{unit_type['Name']}' spots ({facility['Name']}) available at '{js['SelectedPlace']['Name']}'")
        else:
            print(f"No spots available for '{js['SelectedPlace']['Name']}'")
            pass



# location_id = 100
# locations[Ellison, Bear Creek, Kekuli, Mabel Lake, Herald Park]
locations_array=[35,7,57,73,49]
start_date = datetime.datetime(2020,8,21)
# start_date = datetime.datetime.now()
number_of_nights = 1

# for i in range(1, MAX_LOCATION_ID):
for i in locations_array:
    #location_id = 104
    try:
        print_availability_for_location_and_dates(i, start_date, number_of_nights)
    except:
        pass

sys.exit(0)


# for i in range(0, MAX_LOCATION_ID):
#     try:
#         js = get_availability(i, start_date, number_of_nights)
#         if not js:
#             continue
#         # pprint.pprint(js)
#         if js['SelectedPlace']['Available']:
#             print(f"{js['SelectedPlace']['Name']} (id: {js['SelectedPlace']['PlaceId']}) -> {js['SelectedPlace']['Available']}")
#     except Exception as e:
#         pass



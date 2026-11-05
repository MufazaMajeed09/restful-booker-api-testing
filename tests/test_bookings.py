import requests
import json
BASE_URL = "https://restful-booker.herokuapp.com/booking"

def test_get_all_bookings_returns_200():
    response = requests.get("https://restful-booker.herokuapp.com/booking")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_single_booking_has_expected_fields():
    response = requests.get(BASE_URL)
    data = response.json()
    booking_id = data[0]["bookingid"]

    headers = {"Accept": "application/json"}
    response = requests.get(f"{BASE_URL}/{booking_id}", headers=headers)
    assert response.status_code == 200
   

    data = response.json()
  
    data_list = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
    for i in data_list:
        assert i in data

    assert isinstance(data["totalprice"], int) 
    assert type(data["depositpaid"]) is bool   
    assert isinstance(data["bookingdates"], dict)  
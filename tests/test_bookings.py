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

def test_new_booking():

    booking_dict = {
    "firstname":"abc",
     "lastname":"xyz",
     "totalprice":1000,
      "depositpaid":True, 
      "bookingdates":{
        "checkin":"2026-12-08", 
        "checkout":"2026-12-12"
      } 
    }   
    headers = {"Accept": "application/json"}
    resp = requests.post(BASE_URL, json=booking_dict, headers=headers)
    
    assert resp.status_code==200

    saved_data_dict = resp.json()

    assert isinstance(saved_data_dict["bookingid"], int)
    assert saved_data_dict["booking"]["firstname"] == "abc"
    assert saved_data_dict["booking"]["lastname"] == "xyz"
    assert saved_data_dict["booking"]["totalprice"] == 1000

    assert saved_data_dict["booking"]["bookingdates"]["checkin"] == "2026-12-08"
    assert saved_data_dict["booking"]["bookingdates"]["checkout"] == "2026-12-12"

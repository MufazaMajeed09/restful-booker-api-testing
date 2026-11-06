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
  

def test_created_booking_can_be_retrieved():
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
    resp_data= resp.json()
    booking_id = resp_data["bookingid"]
    

    resp = requests.get(f"{BASE_URL}/{booking_id}", headers=headers)
    assert resp.status_code==200
    resp_dict = resp.json()

    assert resp_dict["firstname"] == booking_dict["firstname"]
    assert resp_dict["lastname"] == booking_dict["lastname"]
    assert resp_dict["totalprice"] == booking_dict["totalprice"]
    assert resp_dict["depositpaid"] == booking_dict["depositpaid"]
    assert resp_dict["bookingdates"]["checkin"] == booking_dict["bookingdates"]["checkin"]
    assert resp_dict["bookingdates"]["checkout"] == booking_dict["bookingdates"]["checkout"]

def test_auth_returns_token():
    credentials_dict={
        "username": "admin", 
        "password": "password123"
        }
    
    headers = {"Accept": "application/json"}
    resp = requests.post("https://restful-booker.herokuapp.com/auth", json = credentials_dict,headers= headers) 
    assert resp.status_code == 200

    resp = (resp.json())
    assert "token" in resp
    auth_token = resp["token"]
    assert len(auth_token)>0

def  test_update_booking_with_token(auth_token,created_booking):
    


        booking_id = created_booking
    

        updated_booking_dict = {
        "firstname":"new",
        "lastname":"xyz",
        "totalprice":1000,
        "depositpaid":True, 
        "bookingdates":{
            "checkin":"2026-12-08", 
            "checkout":"2026-12-12"
        } 
        } 
        headers = {
        "Accept": "application/json",
        "Cookie": f"token={auth_token}"
    }
        resp = requests.put(f"{BASE_URL}/{booking_id}", json = updated_booking_dict,headers=headers)
        assert resp.status_code == 200

        resp = requests.get(f"{BASE_URL}/{booking_id}", headers=headers)
        assert resp.status_code==200
        resp_dict = resp.json()

        assert resp_dict["firstname"] == "new"

def test_delete_booking_with_token(auth_token,created_booking):

    
        booking_id = created_booking
        headers = {
        "Accept": "application/json",
        "Cookie": f"token={auth_token}"
    }
        resp = requests.delete(f"{BASE_URL}/{booking_id}",headers=headers)
        assert resp.status_code == 201

        resp = requests.get(f"{BASE_URL}/{booking_id}", headers=headers)
        assert resp.status_code==404










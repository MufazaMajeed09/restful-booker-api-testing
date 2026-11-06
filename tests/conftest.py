import pytest
import requests
import json
BASE_URL = "https://restful-booker.herokuapp.com/booking"


@pytest.fixture
def auth_token():
    credentials_dict = {
        "username": "admin",
        "password": "password123"
    }

    headers = {"Accept": "application/json"}
    resp = requests.post("https://restful-booker.herokuapp.com/auth", json=credentials_dict, headers=headers)
    assert resp.status_code == 200

    resp = (resp.json())
    assert "token" in resp
    auth_token = resp["token"]
    assert len(auth_token) > 0

    return auth_token


@pytest.fixture
def created_booking(auth_token):
    booking_dict = {
        "firstname": "abc",
        "lastname": "xyz",
        "totalprice": 1000,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-08",
            "checkout": "2026-12-12"
        }
    }

    headers = {"Accept": "application/json"}
    resp = requests.post(BASE_URL, json=booking_dict, headers=headers)

    assert resp.status_code == 200

    saved_data_dict = resp.json()

    assert isinstance(saved_data_dict["bookingid"], int)
    assert saved_data_dict["booking"]["firstname"] == "abc"
    assert saved_data_dict["booking"]["lastname"] == "xyz"
    assert saved_data_dict["booking"]["totalprice"] == 1000

    assert saved_data_dict["booking"]["bookingdates"]["checkin"] == "2026-12-08"
    assert saved_data_dict["booking"]["bookingdates"]["checkout"] == "2026-12-12"

    booking_id = saved_data_dict["bookingid"]
    yield booking_id

    headers = {
        "Accept": "application/json",
        "Cookie": f"token={auth_token}"
    }
    requests.delete(f"{BASE_URL}/{booking_id}", headers=headers)
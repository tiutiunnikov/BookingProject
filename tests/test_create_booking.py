import  allure
from pydantic import ValidationError
from core.models.booking import BookingResponse

@allure.feature('Test create booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']

@allure.feature('Test create booking')
@allure.story('Negative: creating booking without required fields')
def test_create_booking_without_required_fields(api_client):
    booking_data = {
        "lastname": "Ivanovich",  # Missed field firstname
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    assert response.status_code == 500, f"Expected status code 400, but got {response.status_code}"
    #error_text = response.json().get('text')
    #assert "Internal Server Error" in error_text, f"Expected error message to mention 'firstname', but got: {error_message}"

    assert response.text == "Internal Server Error"

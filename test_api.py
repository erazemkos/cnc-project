import base64
import os

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_upload_spindle_load_data():
    # Sample data for testing
    machine_number = "M01"
    process_number = "P01"
    label = "good"
    filename = "test_data.h5"

    sample_data = os.urandom(1024)  # Generates 1024 random bytes
    encoded_data = base64.b64encode(sample_data).decode('utf-8')

    # Payload for the test
    payload = {
        "machine_number": machine_number,
        "process_number": process_number,
        "label": label,
        "filename": filename,
        "data": encoded_data
    }

    response = client.post("/upload_spindle_load_data/", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

    # Fetching the last uploaded data
    get_response = client.get(
        "/spindle_load_data/",
        params={"machine_number": machine_number, "process_number": process_number, "label": label}
    )

    # Check if the GET request was successful
    assert get_response.status_code == 200

    data = get_response.json()

    # Comparing the binary data
    returned_data = base64.b64decode(data[-1]['data'])
    assert returned_data == sample_data

test_upload_spindle_load_data()
import base64

import numpy as np
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_upload_spindle_load_data():
    """ Uploads some data to the post endpoint and then gets the same thing and compares """
    # Sample data for testing
    machine_name = "M0123"
    process_name = "P0123"
    label = "good"
    filename = "test_data123.h5"

    random_array = np.random.rand(100, 3).astype(dtype=np.float64)
    random_bytes = random_array.tobytes()
    encoded_data = base64.b64encode(random_bytes).decode('utf-8')

    # Payload for the test
    payload = {
        "machine_name": machine_name,
        "process_name": process_name,
        "label": label,
        "filename": filename,
        "data": encoded_data
    }

    response = client.post("/upload_spindle_load_data/", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

    get_response = client.get(
        "/spindle_load_data/",
        params={"machine_name": machine_name, "process_name": process_name, "label": label}
    )

    # Check if the GET request was successful
    assert get_response.status_code == 200

    data = get_response.json()

    # Comparing the binary data of the last added data with the data that we inserted as a test
    returned_data = base64.b64decode(data[-1]['data'])
    assert returned_data == random_bytes


if __name__ == "__main__":
    test_upload_spindle_load_data()

import base64

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from crud_operations import create_db_handler

app = FastAPI()
db_handler = create_db_handler()


class SpindleLoadData(BaseModel):
    """ Define a Pydantic model for request bodies """
    machine_name: str
    process_name: str
    label: str
    filename: str
    data: str


@app.post("/upload_spindle_load_data/")
async def upload_spindle_load_data(data: SpindleLoadData):
    """
    API endpoint to upload spindle load data.
    """
    # Check if the machine, process, and label already exist in the database
    machine_id = db_handler.get_or_create_machine(data.machine_name)
    process_id = db_handler.get_or_create_process(data.process_name)
    label_id = db_handler.get_or_create_label(data.label)

    # Decode the Base64 encoded data
    data_blob = base64.b64decode(data.data)

    # Insert the spindle load data into the database
    db_handler.create_spindle_load_data(
        machine_id=machine_id,
        process_id=process_id,
        label_id=label_id,
        filename=data.filename,
        data_blob=data_blob
    )

    return JSONResponse(status_code=200, content={"message": "Data uploaded successfully"})


@app.get("/spindle_load_data/")
def get_spindle_load_data(machine_name: str, process_name: str, label: str):
    """
    API endpoint to retrieve spindle load data.
    """
    # Retrieve data from the database
    data = db_handler.get_spindle_load_data(
        machine_name=machine_name,
        process_name=process_name,
        label=label
    )
    if data:
        # Encode binary data to Base64 for JSON response
        for item in data:
            if item.data:
                item.data = base64.b64encode(item.data).decode('utf-8')
        return data
    else:
        raise HTTPException(status_code=404, detail="Data not found")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

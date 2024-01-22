from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pydantic import BaseModel
import base64
import uvicorn

from constants import DATABASE_URL
import models
import crud_operations


app = FastAPI()
engine = create_engine(DATABASE_URL)


class SpindleLoadData(BaseModel):
    """ Define a Pydantic model for request bodies """
    machine_number: str
    process_number: str
    label: str
    filename: str
    data: str


models.Base.metadata.create_all(bind=engine)


@app.post("/upload_spindle_load_data/")
async def upload_spindle_load_data(data: SpindleLoadData):
    """
    API endpoint to upload spindle load data.
    """
    with Session(engine) as session:
        # Check if the machine, process, and label already exist in the database
        machine_id = crud_operations.get_or_create_machine(session, data.machine_number)
        process_id = crud_operations.get_or_create_process(session, data.process_number)
        label_id = crud_operations.get_or_create_label(session, data.label)

        # Decode the Base64 encoded data
        data_blob = base64.b64decode(data.data)

        # Insert the spindle load data into the database
        crud_operations.create_spindle_load_data(
            session,
            machine_id=machine_id,
            process_id=process_id,
            label_id=label_id,
            filename=data.filename,
            data_blob=data_blob
        )

        return JSONResponse(status_code=200, content={"message": "Data uploaded successfully"})


@app.get("/spindle_load_data/")
def get_spindle_load_data(machine_number: str, process_number: str, label: str):
    """
    API endpoint to retrieve spindle load data.
    """
    with Session(engine) as session:
        # Retrieve data from the database
        data = crud_operations.get_spindle_load_data(
            session,
            machine_number=machine_number,
            process_number=process_number,
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

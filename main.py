from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pydantic import BaseModel
import base64

from populate_database import read_h5_file, DATABASE_URL
import models
import crud_operations

# Create a FastAPI instance
app = FastAPI()

# Create a database engine
engine = create_engine(DATABASE_URL)

# Define Pydantic models for request bodies
class SpindleLoadData(BaseModel):
    machine_number: str
    process_number: str
    label: str
    filename: str
    data: str

# Initialize the database and create tables
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
            return data
        else:
            raise HTTPException(status_code=404, detail="Data not found")


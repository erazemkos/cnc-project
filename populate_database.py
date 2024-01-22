import os
import h5py
import numpy as np
from sqlalchemy import create_engine, text
from constants import DATABASE_URL, DATASET_PATH

# Create a database engine
engine = create_engine(DATABASE_URL)
conn = engine.connect()


def read_h5_file(file_path: str):
    """
    Reads an .h5 file and returns the data contained within.
    """
    with h5py.File(file_path, 'r') as f:
        vibration_data = f['vibration_data'][:]
    return vibration_data.astype(np.float64)


def process_and_store_data():
    """
    Processes the CNC machining data and stores it in the sqlite database.
    """

    for machine in get_directories(DATASET_PATH):
        for process in get_directories(os.path.join(DATASET_PATH, machine)):
            for label in get_directories(os.path.join(DATASET_PATH, machine, process)):
                process_label_data(machine, process, label)


def get_directories(path: str, limit: int = 2):
    """
    Returns a list of directory names inside the given path with an upper limit
    """
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs[:limit]


def process_label_data(machine: str, process: str, label: str, extension: str = '.h5'):
    """
    Process and store data for a specific machine, process, and label
    """
    label_path = os.path.join(DATASET_PATH, machine, process, label)
    for filename in os.listdir(label_path):
        if filename.endswith(extension):
            file_path = os.path.join(label_path, filename)
            data = read_h5_file(file_path)

            data_blob = data.tobytes()
            store_data(machine, process, label, filename, data_blob)


def store_data(machine: str, process: str, label: str, filename: str, data_blob: bytes):
    """
    Store the given data in the database
    """
    
    # Prepare the SQL commands as text
    insert_machine = text("INSERT OR IGNORE INTO machines (machine_number) VALUES (:machine)")
    insert_process = text("INSERT OR IGNORE INTO processes (process_number) VALUES (:process)")
    insert_label = text("INSERT OR IGNORE INTO labels (label) VALUES (:label)")
    insert_spindle_load = text("""
        INSERT INTO spindle_load_data 
        (machine_id, process_id, label_id, filename, data) 
        VALUES (:machine_id, :process_id, :label_id, :filename, :data_blob)
    """)

    # Executing each insert and getting the lastrowid
    machine_id = conn.execute(insert_machine, {"machine": machine}).lastrowid
    process_id = conn.execute(insert_process, {"process": process}).lastrowid
    label_id = conn.execute(insert_label, {"label": label}).lastrowid

    # Inserting the spindle load data
    conn.execute(insert_spindle_load, {
        "machine_id": machine_id,
        "process_id": process_id,
        "label_id": label_id,
        "filename": filename,
        "data_blob": data_blob
    })
    conn.commit()


def main():
    """
    Main function to process and store CNC machining data.
    """
    process_and_store_data()
    print("Database filled up.")


if __name__ == "__main__":
    main()

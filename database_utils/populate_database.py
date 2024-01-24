import os

import h5py
import numpy as np

from database_utils.constants import DATASET_PATH
from database_utils.database_handler import create_db_handler, IDatabaseHandler


def read_h5_file(file_path: str) -> np.ndarray:
    """ Reads an .h5 file and returns the data contained within as a numpy array with type float64 """
    with h5py.File(file_path, 'r') as f:
        vibration_data = f['vibration_data'][:]
    return vibration_data.astype(np.float64)


def process_and_store_data(db_handler: IDatabaseHandler):
    """ Processes the CNC machining data and stores it in the sqlite database. """

    for machine in get_directories(DATASET_PATH):
        for process in get_directories(os.path.join(DATASET_PATH, machine)):
            for label in get_directories(os.path.join(DATASET_PATH, machine, process)):
                process_label_data(db_handler, machine, process, label)


def get_directories(path: str, limit: int = 2):
    """ Returns a list of directory names inside the given path with an upper limit """
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs[:limit]


def process_label_data(db_handler: IDatabaseHandler, machine: str, process: str, label: str, extension: str = '.h5'):
    """ Process and store data for a specific machine, process, and label """
    label_path = os.path.join(DATASET_PATH, machine, process, label)
    for filename in os.listdir(label_path):
        if filename.endswith(extension):
            file_path = os.path.join(label_path, filename)
            data = read_h5_file(file_path)

            data_blob = data.tobytes()
            store_data(db_handler, machine, process, label, filename, data_blob)


def store_data(db_handler: IDatabaseHandler, machine: str, process: str, label: str, filename: str, data_blob: bytes):
    """ Store the given data in the database """
    machine_id = db_handler.get_or_create_machine(machine)
    process_id = db_handler.get_or_create_process(process)
    label_id = db_handler.get_or_create_label(label)

    db_handler.create_spindle_load_data(machine_id, process_id, label_id, filename, data_blob)


def main():
    """ Main function to process and store CNC machining data. """
    process_and_store_data(create_db_handler())
    print("Database filled up.")


if __name__ == "__main__":
    main()

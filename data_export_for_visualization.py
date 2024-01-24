import numpy as np
import pandas as pd

from database_utils.database_handler import create_db_handler, IDatabaseHandler


def array_to_csv(array: np.ndarray, filename: str, separator: str = ';'):
    """ Saves a Nx3 dim array as a csv """

    df = pd.DataFrame(array, columns=['x', 'y', 'z'])   # I assume this is the correct order
    df.to_csv(filename, index=False, sep=separator)     # Separator is very important and I believe specific to locale


def export_data_for_visualization(db_handler: IDatabaseHandler, machine_name: str = "M01", process_name: str = "OP01"):
    """ Fetches data for the same machine-process pairs with both 'good' and 'bad' labels and saves it as csv files. """
    good_data = db_handler.get_spindle_load_data(machine_name=machine_name, process_name=process_name, label="good")[0]
    bad_data = db_handler.get_spindle_load_data(machine_name=machine_name, process_name=process_name, label="bad")[0]

    good_data_arr = np.frombuffer(good_data.data, dtype=np.float64)
    bad_data_arr = np.frombuffer(bad_data.data, dtype=np.float64)

    array_to_csv(good_data_arr.reshape(-1, 3), "good_data.csv")
    array_to_csv(bad_data_arr.reshape(-1, 3), "bad_data.csv")


if __name__ == "__main__":
    export_data_for_visualization(db_handler=create_db_handler())

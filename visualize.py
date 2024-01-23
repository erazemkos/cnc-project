import matplotlib.pyplot as plt
import numpy as np

from database_utils.database_handler import create_db_handler, IDatabaseHandler
from database_utils.models import SpindleLoadData


def visualize_data(byte_data: list[SpindleLoadData], machine_name: str, process_name: str, num_samples: int = 5000):
    """ Visualizes the data using Matplotlib with subplots for the same machine-process pairs. """
    # Create a figure with two subplots
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    for i, label in enumerate(['good', 'bad']):
        data = np.frombuffer(byte_data[i].data, dtype=np.float64)
        data_array = data.reshape(-1, 3)
        axes[i].plot(data_array[:num_samples, 0])
        axes[i].plot(data_array[:num_samples, 1])
        axes[i].plot(data_array[:num_samples, 2])
        axes[i].set_title(f"Machine: {machine_name}, Process: {process_name}, Label: {label}")
        axes[i].set_xlabel('Sample Number')
        axes[i].set_ylabel('Data Value')

    plt.tight_layout()
    plt.show()


def visualize_samples(db_handler: IDatabaseHandler, machine_name: str = "M01", process_name: str = "OP01"):
    """
    Fetches data for the same machine-process pairs with both 'good' and 'bad' labels and visualizes it.
    """
    good_data = db_handler.get_spindle_load_data(machine_name=machine_name, process_name=process_name, label="good")[0]
    bad_data = db_handler.get_spindle_load_data(machine_name=machine_name, process_name=process_name, label="bad")[0]

    visualize_data([good_data, bad_data], machine_name, process_name)


if __name__ == "__main__":
    visualize_samples(db_handler=create_db_handler())

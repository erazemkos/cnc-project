import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from crud_operations import create_db_handler


def visualize_data(byte_data, machine_number, process_number):
    """
    Visualizes the data using Matplotlib with subplots for the same machine-process pairs.
    """
    # Create a figure with two subplots
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    for i, label in enumerate(['good', 'bad']):
        data = np.frombuffer(byte_data[i].data, dtype=np.float64)
        data_array = data.reshape(-1, 3)
        axes[i].plot(data_array[:5000, 0])
        axes[i].plot(data_array[:5000, 1])
        axes[i].plot(data_array[:5000, 2])
        axes[i].set_title(f"Machine: {machine_number}, Process: {process_number}, Label: {label}")
        axes[i].set_xlabel('Sample Number')
        axes[i].set_ylabel('Data Value')

    plt.tight_layout()
    plt.show()


def visualize_samples(db_handler, machine_number="M01", process_number="OP01"):
    """
    Fetches data for the same machine-process pairs with both 'good' and 'bad' labels and visualizes it.
    """
    good_data = db_handler.get_spindle_load_data(machine_number=machine_number, process_number=process_number, label="good")[0]
    bad_data = db_handler.get_spindle_load_data(machine_number=machine_number, process_number=process_number, label="bad")[0]

    visualize_data([good_data, bad_data], machine_number, process_number)


if __name__ == "__main__":
    db_handler = create_db_handler()
    visualize_samples(db_handler)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Define the database connection string
DATABASE_URL = "sqlite:///./cnc_machining.db"

# Create a database engine
engine = create_engine(DATABASE_URL)

def process_data_blob(data_blob):
    """
    Processes the data blob and returns a structured format (like a NumPy array).
    Adjust this function based on the actual structure of your data blob.
    """
    # Dummy implementation, replace with actual processing logic
    return np.frombuffer(data_blob, dtype=np.float32)  # Modify dtype as needed

def visualize_data(df):
    """
    Visualizes the data using Matplotlib with subplots for the same machine-process pairs.
    """
    # Create a figure with two subplots
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    for i, label in enumerate(['good', 'bad']):
        label_df = df[df['label'] == label]

        if label_df.empty:
            print(f"No data available for label: {label}")
            continue

        # Process and plot the first 1000 samples of available data
        data = process_data_blob(label_df.iloc[0]['data'])
        axes[i].plot(data[:5000])
        axes[i].set_title(f"Machine: {label_df['machine_number'].iloc[0]}, Process: {label_df['process_number'].iloc[0]}, Label: {label}")
        axes[i].set_xlabel('Sample Number')
        axes[i].set_ylabel('Data Value')

    plt.tight_layout()
    plt.show()


def export_data_for_visualization():
    """
    Fetches data for the same machine-process pairs with both 'good' and 'bad' labels and visualizes it.
    """
    query = """
    SELECT m.machine_number, p.process_number, l.label, sld.filename, sld.timestamp, sld.data
    FROM spindle_load_data sld
    JOIN machines m ON sld.machine_id = m.id
    JOIN processes p ON sld.process_id = p.id
    JOIN labels l ON sld.label_id = l.id
    WHERE (m.machine_number, p.process_number) IN (
        SELECT machine_number, process_number
        FROM spindle_load_data
        JOIN machines ON spindle_load_data.machine_id = machines.id
        JOIN processes ON spindle_load_data.process_id = processes.id
        JOIN labels ON spindle_load_data.label_id = labels.id
        GROUP BY machine_number, process_number
        HAVING COUNT(DISTINCT label) = 2
    )
    AND l.label IN ('good', 'bad')
    ORDER BY m.machine_number, p.process_number, l.label DESC
    """

    df = pd.read_sql_query(query, engine)
    if df.empty:
        print("No data found for the given criteria.")
    else:
        visualize_data(df)


if __name__ == "__main__":
    export_data_for_visualization()

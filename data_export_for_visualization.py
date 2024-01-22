import pandas as pd
from sqlalchemy import create_engine

# Define the database connection string
DATABASE_URL = "sqlite:///./cnc_machining.db"

# Create a database engine
engine = create_engine(DATABASE_URL)

def export_data_for_visualization():
    """
    Exports one 'good' and one 'bad' spindle load data entry from the sqlite database into a CSV file
    for visualization in PowerBI.
    """
    # Query to select one 'good' and one 'bad' data row
    query = """
    SELECT m.machine_number, p.process_number, l.label, sld.filename, sld.timestamp, sld.data
    FROM spindle_load_data sld
    JOIN machines m ON sld.machine_id = m.id
    JOIN processes p ON sld.process_id = p.id
    JOIN labels l ON sld.label_id = l.id
    WHERE l.label IN ('good', 'bad')
    GROUP BY l.label
    """

    # Execute the query and fetch the data
    df = pd.read_sql_query(query, engine)

    # Export the data to a CSV file
    df.to_csv('spindle_load_data_for_visualization.csv', index=False)
    print("Data exported successfully to 'spindle_load_data_for_visualization.csv'")


if __name__ == "__main__":
    export_data_for_visualization()

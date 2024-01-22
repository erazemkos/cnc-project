To run:

1. First clone cnc data to ./data:

`git clone https://github.com/boschresearch/CNC_Machining.git ./data`

2. Create a database using sqlite:

`python .\database_setup.py`

3. Populate the database:

`python .\populate_database.py`

4. Export two examples - one good, one bad:

`python .\data_export_for_visualization.py`

5. Test API by writing an entry to a database using the `/upload_spindle_load_data/` endpoint and then querying it
using the `/spindle_load_data/` and finally comparing the result with the entry that was inteded to be written:

`python test_api.py`
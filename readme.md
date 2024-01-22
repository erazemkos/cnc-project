To run:

1. First clone cnc data to ./data:
`git clone https://github.com/boschresearch/CNC_Machining.git ./data`

2. Create a database using sqlite:
`python .\database_setup.py`

3. Populate the database:
`python .\populate_database.py`

4. Export two examples - one good, one bad:
`python .\data_export_for_visualization.py`


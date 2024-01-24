To run:

1. First clone this repo and cnc data to `./data`:

```
   git clone https://github.com/erazemkos/cnc-project.git
   cd cnc-project
   git clone https://github.com/boschresearch/CNC_Machining.git ./data
```

2. Create a database using sqlite by running a script with the module as a context:

```
   python -m database_utils.database_setup
```

3. Similar to populate the database:

```
   python -m database_utils.populate_database
```

4. Export two examples as csv files - one good, one bad:

```
   python data_export_for_visualization.py
```

OR just visualize it with matplotlib (on a subplot using 4000 samples):

```
    python visualize.py
```

5. Test API by writing an entry to a database using the `/upload_spindle_load_data/` endpoint and then querying it
using the `/spindle_load_data/` and finally comparing the result with the entry that was intended to be written:

```
    python test_api.py
```

OR test manually using requests for example (app is running on `0.0.0.0` on port `8000`). Run main app with:

```
    python main.py
```

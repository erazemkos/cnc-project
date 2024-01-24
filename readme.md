### To run:

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

OR just visualize it with matplotlib (on a subplot using 5000 samples):

```
    python visualize.py
```

5. Test API by writing an entry to a database using the `/upload_spindle_load_data/` endpoint and then querying it
using the `/spindle_load_data/` and finally comparing the result with the entry that was intended to be written. Pytest
should automatically detect all test files. To run tests:

```
    pytest
```

OR test manually using requests for example (app is running on `0.0.0.0` on port `8000`). Run main app with:

```
    python main.py
```

### Additional notes:

1. Data was saved as different formats (different ints and floats) which indicates different sensors and capture protocols used.
I don't think this was documented.

2. Docstrings are not PEP 257-compliant. I find that the type hints combined with clear names of parameters
are sufficient for parameter description, however this is a recent style development. I can modify it.

3. The database_handler.py is the only thing I deemed worthy of making dependancy injection for. The rest of the app is complex enough to
make abstractions of. I believe premature abstraction is the same evil as premature optimization.

4. Data is saved as binary data in the database but that is incompatible with json. This is why I use base64 encoding.
So to post the json, you have to encode the data first.

5. In a real project, test files would be in a separate folder. Also constants could be in a `common` folder or something like that.
But this app is a bit too small for common objects I believe.

6. I didn't use PowerBI for visualization as I didn't really find a need for it. I don't know if that was part of the test or just a suggestion,
so I included the `data_export_for_visualization.py` script which exports two samples to csv files, which I believe can be used in PowerBI.
For this use case I think matplotlib is more than enough though.

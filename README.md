# pytest-by-fixture-marker
pytests by fixture marker

```
usage: python3 tests-by-fx.py [-h] {pipeline,smoke,xfail,skip,all}

Group tests by fixture markers and then show totals.

positional arguments:
  {pipeline,smoke,xfail,skip,all}
                        Specify the pytest marker to search for.

options:
  -h, --help            show this help message and exit
```

to show all marked tests simply run

`python3 tests-by-fx.py all`

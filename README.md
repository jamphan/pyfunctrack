# pyfunctrack
Simple function tracking utility in Python

## Simple Usage

Tracking can be configured through a YAML file. Simply having a `functions:` node with a list of function
configurations will enable tracking for the listed functions.

For example, if we have a script such as:

``` py
import time
import uuid

def get_data():
    time.sleep(1)
    return str(uuid.uuid4())

def count_features(data):
    return len(data.split("\n"))

def main():
    test_data = get_data()
    num_features = count_features(test_data)
    print(num_features)
```

We can define a tracking config like:

``` yaml
trackers:
  logger:
    log_file: ".my_tracker_log"
functions:
  get_data:
    parameter: data
  count_features:
    parameter: n_features
```

And we can then run the script with:

``` bash
python -m pyfunctrack main.py
```

This will produce a `.my_tracker_log` file in your current directory with the output:

``` log
DATA:get_data returned 8ac4b0b8-dc3f-4572-b70e-f844ba457cff and took 1 secs
N_FEATURES:count_features returned 1 and took 0 secs
```
# Testing bhcli

This project comes with a collection of test cases to ensure the tool is properly functioning.
The tests are very simple at the moment and mostly ensure the various subcommands run without exploding.
This is by no means a comprehensive test suite but is probably enough to detect when something fundamentally crashes (e.g. because the BHCE API changed).

## Running the tests

1. Ensure `bhcli` and its development dependencies are installed.

```console
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -e .[dev]
```

2. Start a BloodHound CE instance **without any data** ingested.
If data is ingested, some test cases may fail.
This is also true for repetitive runs of the test suite without clearing the data first.

3. Create a config file `tests/config.ini` based on `tests/config_example.ini` and fill it with the login data for your BloodHound CE instance.

4. Execute the test suite.

```console
$ pytest
```

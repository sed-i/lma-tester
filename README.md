# prometheus-tester

## Description

This charm generates test data for functional testing of the
Prometheus Operator.

## Usage

    juju deploy ./prometheus-tester.charm

## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests

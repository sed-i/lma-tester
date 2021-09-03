# prometheus-tester

## Description

This charm generates test data for functional testing of the
Prometheus Operator.

## Usage
```shell
juju deploy ./prometheus-tester.charm
```

## Developing

Create and activate a virtualenv with the development requirements:
```shell
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

```shell
./run_tests
```

## Building

### Build the application image

Assuming you want to run Prometheus Tester on [MicroK8s](https://microk8s.io/), ensure it has the `registry` plugin active:

```sh
$ microk8s enable registry
```

We will need the MicroK8s registry plugin up and running to store in there the `prometheus-tester` image.

Now, build the `prometheus-tester` image and push it to MicroK8s's registry with:

```sh
(cd tester; docker build . -t localhost:32000/prometheus-tester:latest; docker push localhost:32000/prometheus-tester:latest)
```

The (weirdly-looking) `localhost:32000/` prefix in the image name lets us push easily the prometheus-tester OCI image to the local MicroK8s registry.

### Build charm

```sh
charmcraft pack
```

Depending on the version of `charmcraft` you use (below 1.2.0 or not), the filename of the charm changes.

### Deploy to Juju

```sh
juju deploy <charm_file> prometheus-tester --resource prometheus-tester-image=localhost:32000/prometheus-tester:latest
```

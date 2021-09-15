# lma-tester

## Description

This charm generates test data for functional testing of the
Prometheus Operator.

## Usage
```shell
juju deploy ./lma-tester_ubuntu-20.04-amd64.charm \
  --resource lma-tester-image=ghcr.io/sed-i/lma-tester-alerts:main
```

## Developing

Create and activate a virtualenv with the development requirements:
```shell
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Testing

```shell
tox -e lint
tox -e static
tox -e unit
```

To apply coding style,

```shell
tox -e fmt
```

## Building

### Build the application image

### Build application image for local registry

Assuming you want to run Prometheus Tester on [MicroK8s](https://microk8s.io/),
ensure it has the `registry` plugin active:

```sh
$ microk8s enable registry
```

We will need the MicroK8s registry plugin up and running to store in there the
`lma-tester` image.

Now, build the `lma-tester` image and push it to MicroK8s's registry with:

```sh
cd lma-tester-image && \
  docker build . -t localhost:32000/lma-tester:latest && \
  docker push localhost:32000/lma-tester:latest)
```

The (weirdly-looking) `localhost:32000/` prefix in the image name lets us push
easily the lma-tester OCI image to the local MicroK8s registry.

### Build charm

```sh
charmcraft pack
```

### Deploy to Juju

If using local registry,

```sh
juju deploy <charm_file> lma-tester --resource lma-tester-image=localhost:32000/lma-tester:latest
```

If using ghcr.io registry,

```sh
juju deploy <charm_file> lma-tester --resource lma-tester-image=ghcr.io/sed-i/lma-tester-alerts:main
```

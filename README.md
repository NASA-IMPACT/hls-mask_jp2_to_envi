# HLS Mask JP2 to ENVI

## Requirements

The following are required for development:

- Install Docker
- [Install pre-commit](https://pre-commit.com/#install)

Once pre-commit is installed, install the pre-commit hooks:

```plain
pre-commit install --install-hooks
```

## Building and Testing

To build the Docker image, run the following:

```plain
make build
```

To run tests in Docker, run the following, which will build the Docker image, if
not already built, then run tests, which will take 1-2 minutes to complete:

```plain
make test
```

If you want to manually test the CLI, the easiest way to do so is to first open
an interactive shell in a Docker container, which will also build the Docker
image:

```plain
make bash
```

Then, within the Docker container, install the package, which will also install
the script `mask_jp2_to_envi` on your path, and unzip a file containing sample
jp2 files for using with the script:

```plain
pip3 install -e .[dev,test]
unzip -o tests/*.zip -d /tmp
```

You can then use the sample files with the script as follows:

```plain
mask_jp2_to_envi --input-dir /tmp/*.SAFE/GRANULE/*/ --output-dir /tmp/envi
```

FROM osgeo/gdal:ubuntu-full-3.0.3

# Required for click with Python 3.6
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN : \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    git \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-venv \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

RUN pip3 install \
    --no-cache-dir \
    --no-binary rasterio \
    rasterio==1.2.10 \
    tox==3.28.0 \
    tox-venv==0.4.0

WORKDIR /hls-mask_jp2_to_envi
COPY ./ .

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["tox -r"]

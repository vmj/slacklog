#!/usr/bin/env bash
. ./test/python-images.sh

OUTPUT_DIR="doc/_build"

FULL_OUTPUT_DIR="${PROJECT_DIR}/${OUTPUT_DIR}"

mkdir -p "${FULL_OUTPUT_DIR}"

docker run --rm -it \
       -v "${PROJECT_DIR}":/src:ro \
       -v "${FULL_OUTPUT_DIR}":"/src/${OUTPUT_DIR}":rw \
       -w /src \
       $NEWEST_PYTHON_IMAGE \
       rm -rf "${OUTPUT_DIR}/html" && \
       python3 -m pip install --upgrade python-dateutil sphinx && \
       sphinx-build -a -E -j auto -n -q doc "${OUTPUT_DIR}/html"

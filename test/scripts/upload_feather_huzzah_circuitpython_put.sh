#!/bin/sh
PORT=/dev/ttyUSB0

export MPYCROSS=`realpath ../../../circuitpython_2.2.3/mpy-cross/mpy-cross`

# switch to test sources
cd ../src
# create test source directories on board
find testing -type d | \
        grep -v -E "(^./.git.*|^./.idea|^./.vscode|__pycache__)" | \
        xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay  {}"
# compile source .py files to .mpy
find . -type f -name '*.py' | \
    xargs -n1 -I {} sh -c "echo compiling {} ...; ${MPYCROSS} {}"
# upload bytecode .mpy files
find . -type f -name '*.mpy' | \
        xargs -n1 -I {} sh -c "echo uploading {} ...; ampy --port ${PORT} put {} {}"

#switch to test libraries
cd ../libraries/

# Compile adafruit libraries to bytecode and upload
for SUBMODULE in `find . -mindepth 1 -maxdepth 1 -type d `
do
    cd ${SUBMODULE}
    # create adafruit library directories on board
    find . -mindepth 1 -type d | \
            grep -v -E "(^./.git.*|__pycache__|^./doc.*|^./example.*)" | \
            xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay  {}"
    # compile adafruit library .py files to .mpy
    find . -type f -name '*.py' | \
        grep -v -E "(^./conf.py|^./docs/conf.py|^./setup.py|^./example.*)" | \
        xargs -n1 -I {} sh -c "echo compiling {} ...; ${MPYCROSS} {}"
    # upload adafruit library .mpy files
    find . -type f -name '*.mpy' | \
        xargs -n1 -I {} sh -c "echo uploading {} ...; ampy --port ${PORT} put {} {}"
    cd ../
done

# switch to adafruit_blinka source
cd ../../src

# create adafruit_blinka agnostic package for cross-platform logic
ampy --port $PORT mkdir --exists-okay adafruit_blinka
ampy --port $PORT mkdir --exists-okay adafruit_blinka/agnostic
# upload agnostic.mpy for platform detection
$MPYCROSS adafruit_blinka/agnostic/__init__.py
ampy --port $PORT put adafruit_blinka/agnostic/__init__.mpy adafruit_blinka/agnostic/__init__.mpy
# upload time.mpy for time logic
$MPYCROSS adafruit_blinka/agnostic/time.py
ampy --port $PORT put adafruit_blinka/agnostic/time.mpy adafruit_blinka/agnostic/time.mpy

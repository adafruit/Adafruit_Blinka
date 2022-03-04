#!/bin/sh
# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
PORT=/dev/ttyUSB0

export MPYCROSS=`realpath ../../../micropython/mpy-cross/mpy-cross`

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

find . -mindepth 1 -type d | \
        grep -v -E "(^./.git.*|__pycache__)" | \
        xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay  {}"
# compile adafruit blinka .py files to .mpy
find . -type f -name '*.py' | \
    xargs -n1 -I {} sh -c "echo compiling {} ...; ${MPYCROSS} {}"
# upload adafruit blinka .mpy files
find . -type f -name '*.mpy' | \
    xargs -n1 -I {} sh -c "echo uploading {} ...; ampy --port ${PORT} put {} {}"

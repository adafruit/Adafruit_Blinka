#!/bin/sh

export PORT="/dev/ttyUSB0"
export MPYCROSS=`realpath ../../../micropython/mpy-cross/mpy-cross`
export COPY="cp --parents "
export ROOT="/media/cefn/PYBFLASH/"


# switch to test sources
cd ../src
# compile source .py files to .mpy
find . -type f -name '*.py' | \
    xargs -n1 -I {} sh -c "echo compiling {} ...; ${MPYCROSS} {}"
# upload bytecode .mpy files
find ./ -type f -name '*.mpy' | \
        sed "s|^\./||" | \
        xargs -n1 -I {} sh -c "echo uploading {} ...; ${COPY} {} ${ROOT}"

#switch to test libraries
cd ../libraries/

# Compile adafruit libraries to bytecode and upload
for SUBMODULE in gps # `find . -mindepth 1 -maxdepth 1 -type d `
do
    cd ${SUBMODULE}
    # compile adafruit library .py files to .mpy
    find . -type f -name '*.py' | \
        grep -v -E "(^./conf.py|^./docs/conf.py|^./setup.py|^./example.*)" | \
        xargs -n1 -I {} sh -c "echo compiling {} ...; ${MPYCROSS} {}"
    # upload adafruit library .mpy files
    find ./ -type f -name '*.mpy' | \
            sed "s|^\./||" | \
            xargs -n1 -I {} sh -c "echo uploading {} ...; ${COPY} {} ${ROOT}"
    cd ../
done

# switch to adafruit_blinka source
cd ../../src

# compile adafruit blinka .py files to .mpy
find . -type f -name '*.py' | \
    xargs -n1 -I {} sh -c "echo compiling {} ...; ${MPYCROSS} {}"
# upload adafruit blinka .mpy files
find ./ -type f -name '*.mpy' | \
        sed "s|^\./||" | \
        xargs -n1 -I {} sh -c "echo uploading {} ...; ${COPY} {} ${ROOT}"

#!/bin/sh
PORT=/dev/ttyUSB0

# needs a git repo with micropython sharing a top-level directory
# where make has been run in the mpy-cross directory

# Compile unittest to bytecode
../../micropython/mpy-cross/mpy-cross unittest.py

# filter directories, and create relevant ones on the board
find . -type d -mindepth 1 | \
        grep -v -E "(^./.git|^./.idea|^./.vscode|__pycache__)" | \
        xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay {}"

# put top-level .py modules in place
for NAME in agnostic
do
    echo "Copying ${NAME}.py ..."
    ampy --port ${PORT} put ${NAME}.py ${NAME}.py
done

# put top-level .mpy modules in place
for NAME in unittest
do
    echo "Copying ${NAME}.mpy ..."
    ampy --port ${PORT} put ${NAME}.mpy ${NAME}.mpy
done

# recursively sync folders of nested packages
for NAME in board digitalio mcp microcontroller testing
do
    find ${NAME} -name '*.py'| xargs -n1 -I {} sh -c "echo Copying {} ...; ampy --port ${PORT} put {} {}"
done

cd ../../ # change into folder containing repo

# I2C dependencies
echo "Copying module adafruit_bus_device..."
cd Adafruit_CircuitPython_BusDevice # change into different repo
ampy --port ${PORT} mkdir --exists-okay adafruit_bus_device
ampy --port ${PORT} put adafruit_bus_device/__init__.py adafruit_bus_device/__init__.py
ampy --port ${PORT} put adafruit_bus_device/i2c_device.py adafruit_bus_device/i2c_device.py
cd ../

# Compile BME280 to bytecode
./micropython/mpy-cross/mpy-cross ./Adafruit_CircuitPython_BME280/adafruit_bme280.py

# BME280 dependencies
echo "Copying module adafruit_bme..."
cd Adafruit_CircuitPython_BME280 # change into different repo
ampy --port ${PORT} put adafruit_bme280.mpy adafruit_bme280.mpy
cd ../

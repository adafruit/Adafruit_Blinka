#!/bin/sh
PORT=/dev/ttyUSB0

# filter directories, and create relevant ones on the board
find . -type d -mindepth 1 | \
        grep -v -E "(.(git|idea|vscode)|__pycache__)" | \
        xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay {}"

# put top-level modules in place
for NAME in agnostic unittest
do
    echo "Copying ${NAME}.py ..."
    ampy --port ${PORT} put ${NAME}.py ${NAME}.py
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

# BME280 dependencies
echo "Copying module adafruit_bme..."
cd Adafruit_CircuitPython_BME280 # change into different repo
ampy --port ${PORT} put adafruit_bme280.py adafruit_bme280.py
cd ../

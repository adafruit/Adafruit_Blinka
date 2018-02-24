#!/bin/sh
PORT=/dev/ttyUSB0

# create only relevant directories on the board
find testing -type d | \
        grep -v -E "(^./.git|^./.idea|^./.vscode|__pycache__)" | \
        grep -v -E '^testing/implementation/micropython*' | \
        xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay  {}"

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

# recursively sync module folders excluding packages
# already provided by circuitpython, and excluding
# testing packages targeting micropython
for NAME in testing
do
    find ${NAME} -name '*.py'| \
    grep -v -E '^testing/implementation/micropython*' | \
    grep -v -E '^testing/adafruit_blinka.py' | \
    xargs -n1 -I {} sh -c "echo Copying {} ...; ampy --port ${PORT} put {} {}"
done

cd ../../



# I2C dependencies
echo "Copying module adafruit_bus_device..."
cd Adafruit_CircuitPython_BusDevice # change into different repo
ampy --port ${PORT} mkdir --exists-okay adafruit_bus_device
ampy --port ${PORT} put adafruit_bus_device/__init__.py adafruit_bus_device/__init__.py
ampy --port ${PORT} put adafruit_bus_device/i2c_device.py adafruit_bus_device/i2c_device.py
cd ../

# Compile BME280 to bytecode
./circuitpython_2.2.3/mpy-cross/mpy-cross Adafruit_CircuitPython_BME280/adafruit_bme280.py

# BME280 dependencies
echo "Copying module adafruit_bme..."
cd Adafruit_CircuitPython_BME280 # change into different repo
ampy --port ${PORT} put adafruit_bme280.mpy adafruit_bme280.mpy
cd ../

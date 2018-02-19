#!/bin/sh
PORT=/dev/ttyUSB0

# create only relevant directories on the board
find testing -type d | \
        grep -v -E "(.(git|idea|vscode)|__pycache__)" | \
        grep -v -E '^testing/implementation/micropython*' | \
        xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay  {}"

# put top-level modules in place
for NAME in agnostic unittest
do
    echo "Copying ${NAME}.py ..."
    ampy --port ${PORT} put ${NAME}.py ${NAME}.py
done

# recursively sync module folders excluding packages
# already provided by circuitpython, and excluding
# testing packages targeting micropython
for NAME in testing
do
    find ${NAME} -name '*.py'| \
    grep -v -E '^testing/implementation/micropython*' | \
    grep -v -E '^testing/mcp.py' | \
    xargs -n1 -I {} sh -c "echo Copying {} ...; ampy --port ${PORT} put {} {}"
done

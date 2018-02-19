#!/bin/sh
PORT=/dev/ttyUSB0

# filter directories, and create relevant ones on the board
find testing -type d | \
        grep -v -E "(.(git|idea|vscode)|__pycache__)" | \
        xargs -n1 -I {} sh -c "echo Creating directory {} ...; ampy --port ${PORT} mkdir --exists-okay  {}"

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

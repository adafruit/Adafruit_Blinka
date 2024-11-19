import os
from adafruit_blinka.microcontroller.rp2040_u2if.rp2040_u2if import RP2040_u2if

def init_specific_board(serial):
    os.environ["CURRENT_BOARD_SERIAL"] = serial
    import board
    import busio
    return board, busio

def RP2040_u2if_init(serial):
    os.environ["CURRENT_BOARD_SERIAL"] = serial
    rp= RP2040_u2if()
    rp.open(51966, 16389, serial=serial)
    return rp

def display_connected_rp2040():
    import hid
    for dev in hid.enumerate():
        vendor = dev["vendor_id"]
        product = dev["product_id"]
        if vendor == 0xCAFE and product == 0x4005:
            print(dev)
"""Allwinner A20 pin names"""
# Datasheets and other goodies https://linux-sunxi.org/A20

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin


# Based on section 4.2. GPIO MULTIPLEXING FUNCTIONS in A20 datasheet 

PA2 = Pin(?)  # PB0/UART2_TX/UART0_TX/PB_EINT0
UART2_TX = PA2
PA3 = Pin(?)  # PB1/UART2_RX/UART0_RX/PB_EINT1
UART2_RX = PA3

"""RP2040 pins"""

from microcontroller import Pin

GP0 = Pin(0)
GP1 = Pin(1)
GP2 = Pin(2)
GP3 = Pin(3)
GP4 = Pin(4)
GP5 = Pin(5)
GP6 = Pin(6)
GP7 = Pin(7)
GP8 = Pin(8)
GP9 = Pin(9)
GP10 = Pin(10)
GP11 = Pin(11)
GP12 = Pin(12)
GP13 = Pin(13)
GP14 = Pin(14)
GP15 = Pin(15)
GP16 = Pin(16)
GP17 = Pin(17)
GP18 = Pin(18)
GP19 = Pin(19)
GP20 = Pin(20)
GP21 = Pin(21)
GP22 = Pin(22)
GP23 = Pin(23)
GP24 = Pin(24)
GP25 = Pin(25)
GP26 = Pin(26)
GP27 = Pin(27)
GP28 = Pin(28)
GP29 = Pin(29)

# ordered as spiId, sckId, mosiId (tx), misoId (rx)
spiPorts = (
    (0, GP2, GP3, GP0),
    (0, GP2, GP3, GP4),
    (0, GP2, GP3, GP16),
    (0, GP2, GP7, GP0),
    (0, GP2, GP7, GP4),
    (0, GP2, GP7, GP16),
    (0, GP2, GP19, GP0),
    (0, GP2, GP19, GP4),
    (0, GP2, GP19, GP16),
    (0, GP6, GP3, GP0),
    (0, GP6, GP3, GP4),
    (0, GP6, GP3, GP16),
    (0, GP6, GP7, GP0),
    (0, GP6, GP7, GP4),
    (0, GP6, GP7, GP16),
    (0, GP6, GP19, GP0),
    (0, GP6, GP19, GP4),
    (0, GP6, GP19, GP16),
    (0, GP18, GP3, GP0),
    (0, GP18, GP3, GP4),
    (0, GP18, GP3, GP16),
    (0, GP18, GP7, GP0),
    (0, GP18, GP7, GP4),
    (0, GP18, GP7, GP16),
    (0, GP18, GP19, GP0),
    (0, GP18, GP19, GP4),
    (0, GP18, GP19, GP16),
    (1, GP10, GP11, GP8),
    (1, GP10, GP11, GP12),
    (1, GP10, GP15, GP8),
    (1, GP10, GP15, GP12),
    (1, GP14, GP11, GP8),
    (1, GP14, GP11, GP12),
    (1, GP14, GP15, GP8),
    (1, GP14, GP15, GP12),
)

# ordered as uartId, txId, rxId
uartPorts = (
    (0, GP0, GP1),
    (0, GP0, GP13),
    (0, GP12, GP1),
    (0, GP12, GP13),
    (1, GP4, GP5),
    (1, GP4, GP9),
    (1, GP8, GP5),
    (1, GP8, GP9),
)

# ordered as scl, sda
i2cPorts = (
    (0, GP1, GP0),
    (0, GP1, GP4),
    (0, GP1, GP8),
    (0, GP1, GP12),
    (0, GP5, GP0),
    (0, GP5, GP4),
    (0, GP5, GP8),
    (0, GP5, GP12),
    (0, GP9, GP0),
    (0, GP9, GP4),
    (0, GP9, GP8),
    (0, GP9, GP12),
    (0, GP13, GP0),
    (0, GP13, GP4),
    (0, GP13, GP8),
    (0, GP13, GP12),
    (1, GP3, GP2),
    (1, GP3, GP6),
    (1, GP3, GP10),
    (1, GP3, GP14),
    (1, GP7, GP2),
    (1, GP7, GP6),
    (1, GP7, GP10),
    (1, GP7, GP14),
    (1, GP11, GP2),
    (1, GP11, GP6),
    (1, GP11, GP10),
    (1, GP11, GP14),
    (1, GP15, GP2),
    (1, GP15, GP6),
    (1, GP15, GP10),
    (1, GP15, GP14),
)

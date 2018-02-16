from microcontroller import Pin
for key,val in Pin.iteritems():
    globals()[key]=val
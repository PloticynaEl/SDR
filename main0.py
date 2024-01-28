#!/usr/bin/python2
import SoapySDR

# Enumerate devices
print("SDR devices:")
for d in SoapySDR.Device.enumerate(''):
    print(d)

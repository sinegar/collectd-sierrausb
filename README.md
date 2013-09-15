collectd-sierrausb
==================

Collectd Python plugin to retrieve data from a 4g sierra usb modem using AT commands.

Configuration: 
--------------

    <LoadPlugin python>
            Globals true
    </LoadPlugin>
    
    <Plugin python>
            ModulePath ""
            LogTraces true
            Import "collectd-sierrausb"
    
            <Module collectd-sierrausb>
                    SerialDevice "/dev/ttyUSB3"
                    SerialSpeed 115200
                    Debug False
            </Module>
    </Plugin>

Outputs (result of at!gstatus? AT command):
-------------------------------------------

* temperature: temperature
* frequency: band (e.g. 2100, 900, etc.)
* signal_noise: -dBm rx0
* signal_power: -dBm rx1

It has been tested on sierra 320U over Vodafone-AU 3g connection.

Test: 
--------

* current user must have access to the serial port (default /dev/ttyUSB3)
* $> /usr/sbin/collectd -T -C collectd.conf
* test data is saved under test directory

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

Outputs:
--------

* temperature: temperature
* frequency: band (e.g. 2100, 900, etc.)
* signal_noise: -dBm rx0
* signal_power: -dBm rx1

Source (at!gstatus?):
---------------------

!GSTATUS: 
Current Time:  90551            Temperature: 45
Bootup Time:   26365            Mode:        ONLINE         
System mode:   WCDMA            PS state:    Attached     
WCDMA band:    WCDMA 2100 
WCDMA channel: 10812
GMM (PS) state:REGISTERED       NORMAL SERVICE 
MM (CS) state: IDLE             NORMAL SERVICE 

WCDMA L1 State:L1M_FACH         RRC State:   CELL_FACH      
RX level Carrier 0 (dBm):-71    LAC:         123A (987)
RX level Carrier 1 (dBm):-106   Cell ID:    123456789 (98765432)

Test: 
-----

It has been tested with sierra 320U over Vodafone-AU 3g connection.

* current user must have access to the serial port (default /dev/ttyUSB3)
* $> /usr/sbin/collectd -T -C collectd.conf
* test data is saved under test directory

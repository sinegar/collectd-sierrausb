#!/usr/bin/python

# https://github.com/aegiap/collectd-serial/blob/master/arduino_serial.py
#  http://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package

import collectd
import serial
import time
from os import sep


class SierraSerial:

    def __init__(self):
        self.plugin_name = 'SierraSerial'
        self.speed = 115200
        self.device = '/dev/ttyUSB3'
        self.ser = None
        self.debug = False
        self.timeout = 0.5
        self.plugin_instance = None

        self.set_plugin()

    def open(self):
        try:
            if self.debug:
                collectd.warning('SierraSerial: ' +
                    'trying to connect to %s with speed %s' %
                    (self.device, self.speed))
            self.ser = serial.Serial(self.device,
                                     self.speed,
                                     bytesize = 8,
                                     stopbits = 1,
                                     parity = 'N',
                                     timeout=self.timeout)
        except:
            collectd.warning('SierraSerial: ' +
                'error on the serial device %s with the speed %d' %
                (self.device, self.speed))

        if not self.ser.isOpen():
            self.ser.open()

        #collectd.info('SierraSerial: serial connection is ok')

    def set_plugin(self):
        path_elements = self.device.split(sep)
        self.plugin_instance = path_elements[-1]

    def submit(self, datatype, instance, value):
        """
        Push the data back to collectd.
        """
        cvalue = collectd.Values(plugin='sierraserial')
        cvalue.plugin = self.plugin_name
        cvalue.plugin_instance = self.plugin_instance
        cvalue.type = datatype
        cvalue.type_instance = instance
        cvalue.values = [value, ]
        cvalue.dispatch()

        if self.debug:
            collectd.warning('SierraSerial: data dispatched: %s %.1f' %
                (datatype, value))

    def get_value(self):
        """
        Open the serial port, get the value and treat it.
        Then close the serial port.
        """

        self.open()

        self.ser.write('at!gstatus?\r')
	time.sleep(1)

        status = ''
        while self.ser.inWaiting() > 0:
	    status += self.ser.read(1)

        # this seems to keep the directIP alive 
        self.ser.write('at!scact=1,1\r')

        if self.ser.isOpen():
            self.ser.close()

        if status != '':
            #collectd.info(str(status.split()))
            list = status.split()
            ndx = list.index('Temperature:')
            temperature = float(list[ndx + 1])
            frequency = float(list[ndx + 16])
            signal_noise = float(list[ndx + 41][6:])
            signal_power = float(list[ndx + 49][6:])
            self.submit('temperature', 'gauge', temperature)
            self.submit('frequency', 'gauge', frequency)
            self.submit('signal_noise', 'gauge', signal_noise)
            self.submit('signal_power', 'gauge', signal_power)

    def config(self, obj):
        """
        Get the configuration from collectd
        """
        for child in obj.children:
            if child.key == 'Debug':
                self.debug = True
            elif child.key == 'SerialDevice':
                self.device = child.values[0]
                self.set_plugin()
            elif child.key == 'SerialSpeed':
                self.speed = int(child.values[0])

        collectd.info('SierraSerial: configuration')


sierra = SierraSerial()
collectd.register_config(sierra.config)
collectd.register_read(sierra.get_value)

# microbit-module: KitronikMOVEMotorSensors@1.1.0
# Copyright (c) Kitronik Ltd 2019. 
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from microbit import pin1, pin2, pin13, pin14
import machine
import utime

class MOVEMotorSensors:
    CM_CONVERSION_FACTOR = 0.0343
    INCH_CONVERSION_FACTOR = 2.54
    MAX_DISTANCE_TIMEOUT = int(2 * 500 / CM_CONVERSION_FACTOR)

    # Returns -1 when sensor not fitted
    # Returns -2 when range is over the sensors max distance
    def distanceCm(self):
        pin14.set_pull(pin14.NO_PULL)
        pin13.set_pull(pin13.NO_PULL)
        pin13.write_digital(0)
        utime.sleep_us(2)
        pin13.write_digital(1)
        utime.sleep_us(10)
        pin13.write_digital(0)             
        
        pulse = machine.time_pulse_us(pin14, 1, self.MAX_DISTANCE_TIMEOUT)
        
        if pulse < 0:
            return pulse
        
        return round((pulse * self.CM_CONVERSION_FACTOR) / 2)

    def distanceInch(self):
        return round(self.distanceCm() / self.INCH_CONVERSION_FACTOR)

    def lineFollowCal(self):
        self.rightLineSensor = pin1.read_analog()
        self.leftLineSensor = pin2.read_analog()
        #calculate the middle value between the two sensor readings
        offset = abs(self.rightLineSensor-self.leftLineSensor)/2
        #apply the offset to each reading so that it neutralises any difference
        if self.leftLineSensor > self.rightLineSensor:
            self.leftLfOffset = -offset
            self.rightLfOffset = offset
        else:
            self.leftLfOffset = offset
            self.rightLfOffset = -offset
  
    def readLineFollow(self, sensor):
        if sensor == "left":
            return pin2.read_analog() + self.leftLfOffset
        elif sensor == "right":
            return pin1.read_analog() + self.rightLfOffset

#!/usr/bin/python
import smbus
import math
import time

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

class MPU6050:
    def __init__(self):
        # Power management registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1) 
        self.address = 0x68        # This is the address value read via the i2cdetect command
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
        # Arguments for calculation
        self.gyro_scale  = 100.0
        self.gyro_threshold = 100.0
        self.accel_scale = 16384.0
        

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.read_byte(adr)
        low  = self.read_byte(adr+1) 
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def get_gyro_x_raw(self):
        return self.read_word_2c(0x43)

    def get_gyro_x(self):
        x_raw = self.get_gyro_x_raw()
        if abs(x_raw) < self.gyro_threshold:
            return 0
        else:
            return x_raw/self.gyro_scale

    def get_gyro_y_raw(self):
        return self.read_word_2c(0x45)

    def get_gyro_y(self):
        y_raw = self.get_gyro_y_raw()
        if abs(y_raw) < self.gyro_threshold:
            return 0
        else:
            return y_raw/self.gyro_scale

    def get_gyro_z_raw(self):
        return self.read_word_2c(0x47)

    def get_gyro_z(self):
        z_raw = self.get_gyro_z_raw()
        if abs(z_raw) < self.gyro_threshold:
            return 0
        else:
            return z_raw/self.gyro_scale

    def get_accel_x_raw(self):
        return self.read_word_2c(0x3b)

    def get_accel_x(self):
        return self.get_accel_x_raw()/self.accel_scale

    def get_accel_y_raw(self):
        return self.read_word_2c(0x3d)

    def get_accel_y(self):
        return self.get_accel_y_raw()/self.accel_scale
    
    def get_accel_z_raw(self):
        return self.read_word_2c(0x3f)

    def get_accel_z(self):
        return self.get_accel_z_raw()/self.accel_scale

    def get_x_rotation(self):
        x, y, z = self.get_accel_x(), self.get_accel_y(), self.get_accel_z()
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)
    
    def get_y_rotation(self):
        x, y, z = self.get_accel_x(), self.get_accel_y(), self.get_accel_z()
        radians = math.atan2(x, dist(y,z))
        return math.degrees(radians)

    def print_data(self):
        print "gyro data"
        print "---------"
        print "gyro_xout: ", self.get_gyro_x()
        print "gyro_yout: ", self.get_gyro_y()
        print "gyro_zout: ", self.get_gyro_z()
        print
        print "accelerometer data"
        print "------------------"
        print "accel_xout: ", self.get_accel_x()
        print "accel_yout: ", self.get_accel_y()
        print "accel_zout: ", self.get_accel_z()
        print "x rotation: " , self.get_x_rotation()
        print "y rotation: " , self.get_y_rotation()


if __name__ == '__main__':
    chip = MPU6050()
    while True:
        time.sleep(0.1)
        chip.print_data()

    

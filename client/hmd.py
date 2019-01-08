from mpu6050 import MPU6050
import math
import time
import socket

class HMD:
    def __init__(self):
        self.chip = MPU6050()
        self.interval = 0.1
        self.last_angular_speed = 0
        self.angle = 0
        self.round = 450.0 # change with the scale value and threshold value of gyro in MPU6050
        # for communication
        self.serverIP = '192.168.1.241' # IP of the server raspberryPi
        self.serverPort = 8082

    def update(self):
        current_angular_speed = self.chip.get_gyro_y()
        delta = (current_angular_speed + self.last_angular_speed) * self.interval/2.0
        self.angle += delta
        self.last_angular_speed = current_angular_speed

    def run(self):
        while True:
            time.sleep(self.interval)
            self.update()
            mySocket = socket.socket()
            mySocket.connect((self.serverIP, self.serverPort))
            mySocket.send(str(self.angle/self.round))
            mySocket.close()
            

if __name__ == '__main__':
    hmd = HMD()
    hmd.run()

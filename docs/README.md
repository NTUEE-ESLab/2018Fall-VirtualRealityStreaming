# 2018 Fall Embedded System Final Project

![vr_sample](05.jpg)

## Motivatoin

  Live broadcast is getting more and more popular nowadays, and it became an important part in social media.
  But there's a big problem -- the field of view is highly restricted, the user can only see the part where the broadcaster shows them.
  So we want to craete a new experience in live broadcast, enabling users can interact more with each other.
  
## Introduction

  With the growing popularity of VR (Virtual Reality), we decide to borrow the idea of it, and integrate in the live broadcast. We want to enable user to change their point of view actively while live broadcast, see whereever they want, enjoy more fun with friends.
  We want to make a product as illustration below: the little camera can record videos, and rotates according to the movement of the user's head, and he/she can watch the live video in the HMD (head-mounted display)

![intro](17.PNG)

## Materials

* Raspberry Pi *2
* Pi camera
* Stepper motor
* Head mounted display
* Smartphone
* Internet

## Server site
![server](IMG_4104.JPG)

### target 
  Server records the video, and streams to localhost, therefore others can watch the live broadcast on the browser. Additionally, the camera can rotate according to the user's head movements which might be far away.
  
### Streaming the video
  We use a tool named **mjpeg-streamer** to help us stream on the Raspberry Pi. It can be used to stream JPEG files over IP-based network from a webcam to various browsers. Furthermore, It's written for embedded devices with limited resources  in terms RAM and CPU.

The complete source code can be found on github : [mjpg-streamer](https://github.com/jacksonliam/mjpg-streamer)

One can set up the server by following steps:

#### Preparation
   Fist, check that Raspberry Pi is conneted to Wi-Fi, and record the IP address of two Raspberry Pi.
   To find the IP, simply type command below:
   ``` bash
   $ ifconfig
   ```
   After that, connect the Pi camera to the Raspberry Pi, and type:
   ```bash
   $ sudo raspi-config
   ```
   then enable the camera. 
  
#### Set up the mjpg-streamer
   clone the repo from the website:
   ```
   $ git clone https://github.com/jacksonliam/mjpg-streamer.git
   ```
   
   Next, we have to compile the source codes:
   ```bash
   $ cd mjpg-streamer/
   $ cd mjpg-streamer-experimental/
   $ sudo apt-get install cmake
   $ sudo apt-get install python-imaging
   $ sudo apt-get install libjpeg-dev
   $ make CMAKE_BUILD_TYPE=Debug
   $ sudo make install
   ```
   
   We need to set an environment variable:
   ```bash
   $ export LD_LIBRARY_PATH=.
   ```
   
   Now we can start streaming:
   ```bash
   $ ./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so"
   ```
   
   We can see the video by going to the link in the browser:
   ```
   http://HOSTNAME:8080/?action=stream
   ```
   where the **HOSTNAME** is the IP address of the server Raspberry Pi
   Now we can use smartphone to watch the streaming video, and put it in the HMD.

   reference : https://desertbot.io/blog/how-to-stream-the-picamera

### Make the camera rotate
Equip the server Raspberry Pi eith stepper motor. 
The detail can seen [here](https://blog.everlearn.tw/%E7%95%B6-python-%E9%81%87%E4%B8%8A-raspberry-pi/raspberry-pi-3-model-b-%E5%88%A9%E7%94%A8-uln2003a-28byj-48-%E9%A9%85%E5%8B%95%E6%9D%BF%E6%8E%A7%E5%88%B6%E6%AD%A5%E9%80%B2%E9%A6%AC%E9%81%94)

put the server/motor.py (in guthub repo) in the server. The server receives the signal senr from the client, which tells the **destination** of the camera should be, then the motor rotates according to that.
Note: The 8th line in the motor.py should be modufied so the IP is the server's.

When all is done, run the server/run.sh to make server run.
```bash
bash run.sh
```

> Note: We transmit the **"destination"** instead of **"how much angle should be rotate in this step"** is: if the internet condition is bad, some of the package get lost, the motor can still arrive the correct position.
   
   
## Client site
![client](IMG_4097.JPG)
### Target
   The client detects the head movements, calculates the destination fo the camera should be, and sends to the server.
   
### Preparation
  After the server is already set, use the smartphone to browse to the video, and put it in the HMD.
  
### Detect the head's movement
  We use MPU6050 to detect head motion. There's a gyroscope inside, which can sense the **angular velocity**.
  Note that The component had beter been welded, so the pi can receive the signal successfully.
  
### Angle calculation
  We write a integrator to calculate the destination of the head motion, however, the raw data from the MPU6050 is very unstable. To cpoe with this problem, we use the following method:

**1. Filter:**
When the head motion is relative small, cinsuder the trival angular speed as 0, so the signal sent to the server would be more stable.    
**2. Discretalize:**
We devide the raw value by a scalar, so the signal in a given rage would output the same value (angle velocity). Therefore, the signal would be more stable.

Note: The 2 parameters can be modified in the client/mpu6050.py

### Signal transmition
  We transnit the signal between server and client by **socket**, instead **bluetooth**. Because in real usage, the distance between server and client might be far away, so transmit the signal on the internet is a better choise.

To get the client start, put the codes under client/ in the client server, then type:
```bash
bash run.sh
```
Note: The server IP in client/hmd.py should be modified to the correct server IP.
   
## Demo video
[link](https://www.youtube.com/watch?v=-KDOYl6tp2Y&feature=share)

**Have fun with this project !**

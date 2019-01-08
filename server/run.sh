#sleep 10
#The folowing script should be run after setting up the mjpeg-streamer under this folder
cd mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -hf" &
python motor.py

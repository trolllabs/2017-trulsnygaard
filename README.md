# 2017-trulsnygaard

This repository was used in the protoype development that was the basis for my master's thesis and is intended for specific hardware.
Some of the code may be compatible with other uses. For questions about hardware or help with code, take contact at truls.nygaard@gmail.com or request to read my master's thesis (restricted access until 2019).

This code is intended to be used on a Raspberry Pi.

This repository contains code for:
* tracking pupil (i.e. circle detection optimized for pupil)
* wireless streaming of video (via WIFI), with manipulation possibilites
* serial communication with Arduino
* threading
* image manipulations using OpenCV
  * color convertion
  * blurring
  * thresholding
  * cropping
  * drawing shapes unto images

## Getting started

Guide to installing OpenCV on Raspberry Pi http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
Activate I2C and Picam on the Raspberry pi, attach the master Arduino via USB. 
Run main.py.

## main.py

The main script's function is to initiate the other scripts and to read from the threads they initiate.
The complete program is initiated by running 
> python main.py

and the argument parser lets the user change the run commands. This means that it is possible to disconnect the Arduino by typing
> python main.py -a 0

or changing resolution by typing
> python main.py -x 320 -y 240

and more. Read the code for all options.

## DetectPupil.py

DetectPupil.py contains the class DetectPupil. The class initiates a thread for the update() function when the start() function is called. 
This function detects the pupil and sends byte information about the position to the Arduino, via Serial.

The position can be read with the read() function. This function returns raw position (x,y), position converted for displaying gaze unto the display (x_conv,y_conv) and the image frame.

### Using the Pupil tracker on its own

Import, initiate, loop:

```
 from DetectPupil import DetectPupil
 pupil = DetectPupil((resx,resy),FPS,arduino,left, right, lower, upper)
 pupil.start()
 while True:
   x,y,x_conv,y_conv,r,frame = pupil.read()   

   if cv2.waitKey(1) & 0xFF == ord('q'):
      pupil.stop()
      break
```
DetectPupil() initiation variables are:
* resolution
* Framerate
* Arduino connection? 1/0, true/false
* Number of pixels to crop from the frame (left = 200 means to crop 200 pixels of left side of image)

## wireless.py

Wireless.py connects to wireless WIFI camera that streams the video on a local network. The Raspberry Pi must be connected to the wifi network of the camera, and this script reads the stream from "http://192.168.2.1/?action=stream".

This script can be used in general cases to read an arbitrary video stream from a webpage. Find the adress of the video stream (should look somewhat like the above adress) and insert into code.

## calibrate.py

calibrate.py is used for cropping the image frame of of the camera that tracks the eye and is initiated by typing 
>python main.py -cb 1.

This script changes the cropping of the image frame by use of the trackbars.

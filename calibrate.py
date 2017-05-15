from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import numpy as np
import time

class calibrate:

        def __init__(self,left,right,lower,upper):
		self.camera = PiCamera()
		self.camera.resolution = (640,480)
		self.r = 45
		self.camera.framerate = 32
		self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)
		self.resx,self.resy=self.camera.resolution
                self.upper = upper
                self.lower = lower
                self.left = left
                self.right = right
		self.frame = None
		self.x = 0
		self.y = 0
		self.radius = 0
		self.stopped = False
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.avglen = 50
		self.xstorage = np.zeros((self.avglen,), dtype = np.int)
		self.ystorage = np.zeros((self.avglen,), dtype = np.int)
		cv2.namedWindow("trackbar")
		cv2.resizeWindow("trackbar",256,240*(1024/2)/640)
		cv2.createTrackbar("left","trackbar",  self.left,self.resx,self.nothing)
                cv2.createTrackbar("right","trackbar",self.right,self.resx,self.nothing)
                cv2.createTrackbar("lower","trackbar",self.lower,self.resy,self.nothing)
                cv2.createTrackbar("upper","trackbar",self.upper,self.resy,self.nothing)

	def update(self):
		for f in self.stream:
                        frame = f.array
                        if frame is not None:
                                self.left = cv2.getTrackbarPos("left","trackbar")
                                self.right = cv2.getTrackbarPos("right","trackbar")
                                self.lower = cv2.getTrackbarPos("lower","trackbar")
                                self.upper = cv2.getTrackbarPos("upper","trackbar")
                                frame = cv2.flip(frame,0)
                                if self.left is not -1:
                                        frame = frame[self.lower:self.upper,self.left:self.right]
                                                
                                self.frame=frame
                                self.rawCapture.truncate(0)
                                
                                if self.stopped:
                                        self.stream.close()
                                        self.rawCapture.close()
                                        self.camera.close()			
			
	def start(self):
		Thread(target=self.update, args=()).start()
		return self

        def nothing(x,y):
                pass
	

        def calibrate(self):
                while True:
                        if self.frame is not None:
                                cv2.imshow("trackbar",self.frame)
                        if cv2.waitKey(33) & 0xFF == ord(' '):
                                self.stop()
                                print(self.left,self.right,self.lower,self.upper)
                                break
                
                return self.left,self.right,self.lower,self.upper

        def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		cv2.destroyAllWindows()

        
    
        

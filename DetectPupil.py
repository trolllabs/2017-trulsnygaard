from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2, serial
 
class DetectPupil:
	def __init__(self, resolution, framerate,arduino,left, right, lower, upper):
		self.arduino = arduino
		self.r = 7
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
		self.resx,self.resy=resolution
		self.upper = upper
		self.lower = lower
		self.left = left
		self.right = right
		self.frame = None
		self.x = 0
		self.y = 0
		self.x_conv = 0
		self.y_conv = 0
		self.radius = 0
		self.stopped = False
		self.blink = 1
		
                if self.arduino:
                        self.write = True
                        self.connected = False
                        self.ser = serial.Serial("/dev/ttyACM0",9600,rtscts=1)
                        while not self.connected:
                            serin = self.ser.read()
                            self.connected = True
                else:
                        self.write = False

	def start(self):
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		for f in self.stream:
			frame = f.array	
			frame = cv2.flip(frame,0)
			frame = frame[self.lower:self.upper,self.left:self.right]
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (self.r, self.r), 0)
			#(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
			#low = minVal+20	
			#_,gray = cv2.threshold(gray, low, 255, cv2.THRESH_BINARY) 
			circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,1000,param1=20,param2=15,minRadius=20,maxRadius=30)

			if circles is not None:
				self.blink = 0
				for i in circles[0,:]:
					self.x = i[0]
					self.y = i[1]
					self.x_conv = int(i[0]*640/(self.upper-self.lower))
					self.y_conv = int(i[1]*480/(self.right-self.left))
					self.radius = i[2]
					if self.write:
						x_pos= int(self.x/(self.right-self.left)*255)
						y_pos= int(self.y/(self.upper-self.lower)*255)
						self.ser.write(str.encode('%3d%3d%1d' % (x_pos,y_pos,self.blink)))
			elif circles is None:
				self.blink = 1
				if self.write:
                                        x_pos= int(self.x/(self.right-self.left)*255)
					y_pos= int(self.y/(self.upper-self.lower)*255)
					self.ser.write(str.encode('%3d%3d%1d' % (x_pos,y_pos,self.blink)))

			self.frame=frame
			self.rawCapture.truncate(0)

			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				if self.arduino:
					self.ser.write(str.encode('%3d%3d%1d' % (90,90,1)))
					self.ser.close()
				return
	
	def read(self):
		return self.x,self.y,self.x_conv,self.y_conv,self.radius,self.frame
 
	def stop(self):
		self.stopped = True

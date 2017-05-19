import numpy as np
import cv2
from urllib import request
from threading import Thread


class stream:

    def __init__(self,URL="http://192.168.2.1/?action=stream"):
        self.URL = URL
        self.stream = request.urlopen(self.URL)
        self.byte = b""
        self.stopped = False
        self.image = None

    def update(self):
        while True:
            self.byte += self.stream.read(1024)
            a = self.byte.find(b"\xff\xd8")
            b = self.byte.find(b"\xff\xd9")
            if a!=-1 and b!=-1:
                jpg = self.byte[a:b+2]
                self.byte = self.byte[b+2:]
                self.image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1)
            if self.stopped:
                return
    
    def start(self):
    	Thread(target=self.update, args=()).start()
    	return self


    def read(self):
        return self.image

    def stop(self):
            self.stopped = True

cv2.destroyAllWindows()

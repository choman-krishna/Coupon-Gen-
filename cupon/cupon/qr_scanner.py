import cv2
import threading
from pyzbar.pyzbar import decode 


class VideoCamera(object):
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.ret, self.frame = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.frame.release()

    def get_frame(self):
        
        img = self.frame
        _, jpeg = cv2.imencode('.jpeg', img)


        # Qr Scanning Start

        

        # Qr Scanning ends


        return jpeg.tobytes()
    
    def update(self):
        while True:
            self.ret, self.frame = self.video.read()
             

import cv2
import threading
from pyzbar.pyzbar import decode 


class VideoCamera(object):
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.ret, self.frame = self.video.read()
        self.qr_scanned = False
        threading.Thread(target=self.update, args=()).start()

    def release_camera(self):
        self.video.release()

    def get_frame(self):
        
        img = self.frame
        _, jpeg = cv2.imencode('.jpeg', img)


        # Qr Scanning Start

        for i in decode(img):
            print(i.type)
            print(i.data.decode('utf-8'))
            self.qr_scanned = True

            cv2.waitKey(3)

            

        # Qr Scanning ends


        return jpeg.tobytes(), self.qr_scanned
    
    def update(self):
        while True:
            self.ret, self.frame = self.video.read()
             

import cv2
import threading
from pyzbar.pyzbar import decode 
from services.models import Service


class VideoCamera(object):

    
    scanned_otp = None    
    coupon_status = None
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        _, self.frame = self.video.read()
        self.qr_scanned = False

        self.thread_flag = True

        threading.Thread(target=self.update, args=()).start()

    def release_camera(self):
        self.video.release()
        self.thread_flag = False

    def get_frame(self):
        
        img = self.frame
        _, jpeg = cv2.imencode('.jpeg', img)


        # Qr Scanning Start

        self.qr_data = ''

        for i in decode(img):
            self.qr_data = i.data.decode('utf-8')
            self.qr_scanned = True
                  

        # Qr Scanning ends

        self.data_list = self.qr_data.split(',')
        if self.qr_scanned and len(self.data_list) == 3:
            self.scanned_otp = self.data_list[2]
            self.check_qr(self.scanned_otp)
            self.release_camera()
            


        return jpeg.tobytes(), self.qr_scanned


    def check_qr(self,otp):
        service_db = Service.objects.filter(coupon_id = otp)
        if service_db.exists() and service_db.first().status == False:
            Service.objects.filter(coupon_id = otp).update(status = True)

            self.coupon_status = "PASS"
            self.scanned_otp = otp
        else:
            self.coupon_status = "False"
        
    
    def update(self):
        try:
            while self.thread_flag:
                _, self.frame = self.video.read()
        except:
            pass
             

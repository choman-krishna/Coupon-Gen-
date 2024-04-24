import cv2
import threading
from pyzbar.pyzbar import decode 
from services.models import QrData, Service


class VideoCamera(object):

    thread_flag = True
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        _, self.frame = self.video.read()
        self.qr_scanned = False
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

            cv2.waitKey(3)                     

        # Qr Scanning ends

        self.data_list = self.qr_data.split(',')
        if self.qr_scanned and len(self.data_list) == 3:
            data_db = QrData(name=self.data_list[0], otp=self.data_list[2])
            data_db.save()
            self.check_qr()
            self.release_camera()
            


        return jpeg.tobytes(), self.qr_scanned


    def check_qr(self):
        qr_db = QrData.objects.last()
        service_db = Service.objects.filter(coupon_id=qr_db.otp)
        if service_db.exists() and service_db.first().status == False:
            Service.objects.filter(coupon_id=qr_db.otp).update(status = True)
            print('Exists')
        else:
            print("not")
        
    
    def update(self):
        try:
            while self.thread_flag:
                _, self.frame = self.video.read()
        except:
            pass
             

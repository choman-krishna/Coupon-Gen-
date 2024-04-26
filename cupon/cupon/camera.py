import cv2
import threading
from cupon.qr_scanner import QRScanner

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        _, self.frame = self.video.read()
        self.thread_flag = True
        self.qr_scanner = QRScanner()

        threading.Thread(target=self.update, args=()).start()

    def release_camera(self):
        self.video.release()
        self.thread_flag = False

    def get_frame(self):
        _, jpeg = cv2.imencode('.jpeg', self.frame)
        return jpeg.tobytes()

    def update(self):
        try:
            while self.thread_flag:
                _, self.frame = self.video.read()
                status, otp = self.qr_scanner.scan_qr(self.frame)
                if status == "PASS":
                    self.coupon_status = status
                    self.scanned_otp = otp
        except:
            pass

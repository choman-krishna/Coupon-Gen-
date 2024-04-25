from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators import gzip

from cupon import qr
from cupon import otp_Gen
from services.models import Service, EventList
from cupon import qr_scanner
from cupon.qr_scanner import VideoCamera

def homePage(request):
    return render(request, 'home_page.html')

def genCoupon(request):
    form_data = []
    img_path = ''
    try:
        if request.method == "POST":
            name = request.POST.get('Name')
            event = request.POST.get('Event')
            otp = otp_Gen.generate_random_otp()

            form_data.append(name)
            form_data.append(event)
            form_data.append(otp)
            img_path = qr.gen_qr(form_data,otp)

            data_db = Service(name=name, event = event, coupon_id = otp, qr_img = img_path)
            data_db.save()

            return HttpResponseRedirect('/coupon/')
    except:
        pass

    event_db = EventList.objects.all()
    return render(request,"gen_coupon.html", {'event_data': event_db})



def coupon(request):

    service_data = Service.objects.latest('created_at') 
    event_db = EventList.objects.get(event_name = service_data.event)

    return render(request, 'coupon.html', {'qr_data': service_data, "d_m_y": event_db})


def viewCoupons(request):
    service_data = Service.objects.all() 
    return render(request, 'view-coupon.html', {'coupon_data': service_data})


# Camera Streaming 

def scan_qr(request):        
    return render(request, 'camera.html')



@gzip.gzip_page   
def cameraView(request):    
    stat = False
    cam = qr_scanner.VideoCamera()
    return StreamingHttpResponse(gen(cam, stat), content_type = "multipart/x-mixed-replace;boundary=frame")



def gen(camera, stat):
    
    while not stat:
        frame, stat = camera.get_frame()
        if stat:
            yield b'--text \r\n' + b'Content-Type: text/plain\r\n\r\n' + b'Hello\r\n\r\n'
        yield (b'--frame \r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def check_status(request):
    return JsonResponse({'c_stat' : VideoCamera.coupon_status})
        

# def check_qr():
#     qr_db = QrData.objects.last()
#     service_db = Service.objects.filter(coupon_id=qr_db.otp)
#     if service_db.exists() and service_db.first().status == False:
#         Service.objects.filter(coupon_id=qr_db.otp).update(status = True)
#         return HttpResponseRedirect('/display/')
#     else:
#         print("not")


def displayStatus(request):
    return render(request, 'displayStatus.html')
        


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from cupon import qr
from cupon import otp_Gen
from services.models import Service

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
    return render(request,"gen_coupon.html")



def coupon(request):
    service_data = Service.objects.latest('created_at')
    return render(request, 'coupon.html', {'qr_data': service_data})

def aboutUs(request):
    return HttpResponse("Welcome to Coupon")
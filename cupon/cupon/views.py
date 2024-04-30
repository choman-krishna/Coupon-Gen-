# Import basic http and shortcuts
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render, redirect

# For Streaming 
from django.views.decorators import gzip

# Import the Session
from django.contrib.sessions.models import Session

# Models
from services.models import Service, EventList, ScannedData, GenScanStatus, UsnApproval


# Login & Register 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# To create user
from services.forms import CreateUserForm

# To import Decorators 
from cupon.decorators import unauthenticated_user, allowed_admin, allowed_user

# Import Groups 
from django.contrib.auth.models import Group

# Defined Functions 
from cupon import qr_generator
from cupon import otp_Gen
from cupon import qr_scanner
from cupon.qr_scanner import VideoCamera


# Home Page
@login_required(login_url='/login/')
# @allowed_admin(allowed_roles=['admin'])
@allowed_user()
def homePage(request):
    
    gen_status = GenScanStatus.objects.filter(name="generator").first().status
    scan_status = GenScanStatus.objects.filter(name="scan").first().status
    content ={
        'gen': gen_status,
        'scan': scan_status
    }

    return render(request, 'home_page.html', content)

# Generate Coupon
@login_required(login_url='/login/')
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
            img_path = qr_generator.gen_qr(form_data,otp)

            data_db = Service(name=name, event = event, coupon_id = otp, qr_img = img_path)
            data_db.save()

            # Redirect to Display Coupon
            return HttpResponseRedirect('/coupon/')
    except:
        pass
    
    # Event database
    event_db = EventList.objects.all()
    return render(request,"user_templates/gen_coupon.html", {'event_data': event_db})

# To Display Coupon
@login_required(login_url='/login/')
def coupon(request):

    service_data = Service.objects.latest('created_at') 
    event_db = EventList.objects.get(event_name = service_data.event)

    return render(request, 'user_templates/coupon.html', {'qr_data': service_data, "d_m_y": event_db})

# Table of Coupon
@login_required(login_url='/login/')
def viewCoupons(request):
    service_data = Service.objects.all() 

    return render(request, 'user_templates/view-coupon.html', {'coupon_data': service_data})


# Register 
def register_user(request):
    forms = CreateUserForm()

    if request.method == 'POST':
        forms = CreateUserForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            messages.success(request, 'Account was created for ' + forms.cleaned_data.get('username'))

            
            usn = request.POST.get("usn")
            username = request.POST.get("username")

            user_approval = UsnApproval(name=username, usn=usn)
            user_approval.save()

            group = Group.objects.get(name = 'users')
            user.groups.add(group)
            
            return redirect('/login/')

    content = {'forms': forms}
    return render(request, 'register.html', content)


# Login 
@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session['scanned_otp'] = 'nothing'
            request.session['scan_status'] = False
            request.session.save()
            return redirect('/generator/')
        else:
            messages.success(request, "User name or Password is incorrect")
    return render(request, 'login.html')

# Logout
def logout_user(request):
    logout(request)
    return redirect('/login/')


# Camera Display Page
@login_required(login_url='/login/')
def scan_qr(request):

    get_scan = GenScanStatus.objects.filter(name="scan").first()
    status = get_scan.status
    if status:
        global cam 
        cam = VideoCamera()    

        return render(request, 'user_templates/camera_view.html')
    else:
        return HttpResponse("Dont have Access")



# Camera Streaming Logic
@gzip.gzip_page   
def cameraView(request):   
    stat = False
    global cam
    stream = StreamingHttpResponse(gen(request, cam, stat), content_type = "multipart/x-mixed-replace;boundary=frame")
       
    
    return stream



def gen(request, camera, stat):
    
    while not stat:
        frame, stat, scanned_otp, coupon_status = camera.get_frame()
        if stat:
            request.session['scan_status'] = stat
            request.session.save()
            scanned_db = ScannedData(username = request.session['username'], scanned_otp = scanned_otp, otp_status = coupon_status)
            scanned_db.save()
            return
        else:
            request.session['scan_status'] = False
            request.session.save()
        yield (b'--frame \r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

from django.http import JsonResponse

def  displayStatus(request):
    
    resent_scan = ScannedData.objects.filter(username = request.session['username']).order_by('scanned_time').last()
    

    if resent_scan != None:
         otp_status = resent_scan.otp_status
    else:
        otp_status = 'Not Yet Scanned'
    

    if 'scan_status' in request.session:
        scanned_status = request.session['scan_status']
        print(scanned_status)
    else:
        scanned_status = None 
        print(scanned_status)
    
    display_status = {
        'otp_status': otp_status,
        'scanned_status' : scanned_status
    }
    return JsonResponse(display_status)

def resetSession(request):

    content = {
        "status": request.session['scan_status']
    }
    request.session['scan_status'] = False
    request.session.save()

    return render(request, "displayStatus.html", content)


def offCamera(request):
    global cam 
    cam.release_camera()
    return JsonResponse({"res" : "Camera Off"}) 


# Admin Page

def adminPage(request):

    gen_db = GenScanStatus.objects.all()
    data = {
        "gen_status": str(gen_db[0].status).lower(),
        "scan_status": str(gen_db[1].status).lower()
    }
    
    return render(request, 'admin_home_page.html', data)

# Toggle gen and scan

def genStatus(request):

    if request.method == 'GET':

        is_toggle = request.GET.get("is_toggle")
        name = request.GET.get("toggle_name")

        is_toggle = True if is_toggle == 'true' else False
        
        gen_data = GenScanStatus.objects.filter(name=name).first()
        
        
        gen_data.status = is_toggle 
        gen_data.save()

    return JsonResponse({"res": "Change Updated"})


def addEvent(request):

    if request.method == 'POST':
        event_name = request.POST.get("Event")
        date = request.POST.get("Date")

        is_present = EventList.objects.filter(event_name=event_name).exists()
        
        if not is_present:
            add_event = EventList(event_name=event_name, date = date)
            add_event.save()
        else:
            print("Already Present")
        

    event_data = EventList.objects.all()

    return render(request, 'addEvent.html', {'event_data' : event_data})

# Approval List
def approvalList(request):

    



    

    approved_list = UsnApproval.objects.filter(approval_status=True)
    not_approved_list = UsnApproval.objects.filter(approval_status=False)

    content = {"approved": approved_list, "not_approved": not_approved_list}
    return render(request, "approve_list.html", content)

def approveBlock(request):

    if request.method == 'GET':
        name = request.GET.get("username")
        action = request.GET.get("action")

        UsnApproval.objects.filter(name=name).update(approval_status = True if action == "approve" else False)

    return JsonResponse({"res": "Change Updated"})


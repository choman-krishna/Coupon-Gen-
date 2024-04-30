from django.http import HttpResponse
from django.shortcuts import redirect, render
from services.models import UsnApproval

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('/generator/')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_admin(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None 
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == allowed_roles[0]:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You dont belong here')
                
                
        return wrapper_func
    return decorator

def allowed_user():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            usn = UsnApproval.objects.filter(name=request.user).first()
            print(request.user)
            
            if request.user.groups.exists():
                
                if usn and usn.approval_status == True:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, "templates/askApproval.html")
                
                
        return wrapper_func
    return decorator

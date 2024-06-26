"""
URL configuration for cupon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cupon import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homePage),
    path('generator/', views.genCoupon),
    path('admin/', admin.site.urls),
    path('coupon/', views.coupon),
    path('viewCoupons/', views.viewCoupons),
    path('check/', views.scan_qr) ,
    path('cameraOn/', views.cameraView),
    path('display/', views.displayStatus),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('register/', views.register_user),
    path('resetSession/', views.resetSession),
    path('offCamera/', views.offCamera),
    path('adminPage/', views.adminPage),
    path('genStatus/', views.genStatus),
    path('addEvent/', views.addEvent),
    path('approvalList/', views.approvalList),
    path('approveBlock/', views.approveBlock)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
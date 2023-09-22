from django.urls import path,include
from accounts.views import *
from rest_framework import routers
from knox.views import LogoutView



router = routers.DefaultRouter()
router.register(r'user-register', RegisterView, basename='task')



urlpatterns = [ 
    path('',include(router.urls)),
    path('send_otp/',SendOTP.as_view()),
    path('verify_otp/',VerifyOTP.as_view()),
    path('logout/', LogoutView.as_view(), name='knox_logout')
]

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from accounts.serializers import RegisterSerializer
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework import  status
from rest_framework.decorators import api_view
import random
from django.core.cache import cache

User = get_user_model()

# @api_view(['GET', 'POST'])
# def redis_test(request, *args, **kwargs):
#     redis_instance = redis.StrictRedis(host = settings.REDIS_HOST,port = settings.REDIS_PORT, db=0 )
#     items = {}
#     count = 0
#     for key in redis_instance.keys("*"):
#         items[key.decode("utf-8")] = redis_instance.get(key)
#         count += 1
#     response = {
#             'count': count,
#             'msg': f"Found {count} items.",
#             'items': items
#     }
#     return Response(response, status=200)


class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'response': serializer.data,
            'success': True,
            'message': 'user created',
            'status': status.HTTP_200_OK
        })


class SendOTP(APIView):

    def post(self,request,*args,**kwargs):
        try:
            phone = request.data.get('phone')
            phone = str(phone)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                data = user.first()
                old_otp = data.otp
                if cache.get(phone):
                    #already in cache meaning otp has not expired
                    new_otp = old_otp
                else:
                    new_otp = otp_generator()
                    cache.set(phone,new_otp,20)

                if old_otp:
                    data.otp = new_otp
                    data.save()
                    return Response({
                        'message':'OTP generated',
                        'status': status.HTTP_200_OK

                    })

        except Exception as e:
            return Response({
                'response': f"error occured {e}",
                "status": status.HTTP_400_BAD_REQUEST
            })


class VerifyOTP(APIView):

    def post(self,request,*args,**kwargs):
        try:
            phone = request.data.get('phone')
            otp = request.data.get('otp')
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                data = user.first()
                if data.otp == otp:
                    # login 
                    #login()
                    return Response({
                        'message':'otp vaified',
                        'status': status.HTTP_200_OK
                    })
                else:
                    return Response({
                        'message':'otp not verified',
                        'status': status.HTTP_200_OK
                    })
            return Response({
                'message':'user does not match with db',
                'status': status.HTTP_200_OK
            })
        except Exception as e:
            pass
            






def otp_generator():
    key = random.randint(1, 999999)
    print(key)
    #Klass = instance.__class__
    #qs_exists = Klass.objects.filter(key=key).exists()
    #if qs_exists:
        #return otp_generator()
    return key





# logout api view
# class LogoutView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def post(self, request, format=None):
#         try:
#             request.user.auth_token.delete()
#             return Response({
#                 'message': 'Logout successfully',
#                 'status': status.HTTP_200_OK,
#             })
#         except Exception as e:
#             return Response({
#                 'message': str(e),
#                 'status': status.HTTP_400_BAD_REQUEST,
#             })

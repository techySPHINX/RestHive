from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from api.models import CustomUser
from api.serializers import CustomUserSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.oath import totp
import requests as http_requests

class SignUpView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class GoogleSignInView(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
            email = idinfo['email']
            name = idinfo['name']
            user, created = CustomUser.objects.get_or_create(email=email, defaults={'username': email, 'first_name': name})
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except ValueError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class RecaptchaVerificationView(APIView):
    def post(self, request):
        recaptcha_response = request.data.get('recaptcha_response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = http_requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            return Response({'success': True})
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
def send_otp_via_sms(phone_number, otp):
   
    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=settings.TWILIO_FROM_NUMBER,
        to=phone_number
    )
    
class VerifyOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        try:
            user = CustomUser.objects.get(id=user_id)
            device = TOTPDevice.objects.get(user=user, name='default')
            if device.verify_token(otp):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid OTP'}, status=401)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    
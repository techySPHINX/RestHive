from django.urls import path
from .views import SignUpView, LoginView, GoogleSignInView, RecaptchaVerificationView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('google-signin/', GoogleSignInView.as_view(), name='google_signin'),
    path('verify-recaptcha/', RecaptchaVerificationView.as_view(), name='verify_recaptcha'),
]
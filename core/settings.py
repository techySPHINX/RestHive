INSTALLED_APPS = [
    # ...
    'rest_framework',
    'corsheaders',
    'api',
    'rest_framework_simplejwt',
    'authentication',
    'payments',
    'pdf_generator',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'two_factor.plugins.phonenumber',
    'phonenumber_field',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
    'middleware.custom_middleware.CustomMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {
      'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your_secret_key',
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


CORS_ALLOW_ALL_ORIGINS = True  # For development only

STRIPE_SECRET_KEY = 'your_stripe_secret_key'
STRIPE_PUBLIC_KEY = 'your_stripe_public_key'

GOOGLE_CLIENT_ID = 'your_google_client_id'
GOOGLE_CLIENT_SECRET = 'your_google_client_secret'

RECAPTCHA_SECRET_KEY = 'your_recaptcha_secret_key'

AUTH_USER_MODEL = 'api.CustomUser'

TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_FROM_NUMBER = 'your_twilio_from_number'
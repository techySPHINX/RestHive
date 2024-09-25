from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}
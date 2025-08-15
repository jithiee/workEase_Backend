from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'user_type']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data['user_type'],
            is_active=False,
        )
        user.generate_otp()  # This generates and sends OTP
        return user

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get("phone_number")
        otp = attrs.get("otp")

        try:
            user = CustomUser.objects.get(phone_number=phone)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        user.is_verified = True
        user.otp = None
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_verified:
            raise serializers.ValidationError("User not verified via OTP")
        return user

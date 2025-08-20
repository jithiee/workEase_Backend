from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

#-------Register Serializer-------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'user_type', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create(
            **validated_data,
            is_active=False,
            is_verified=False,
        )
        user.set_password(password)
        user.save()
        return user
    
#------------ VerifyOTP Serializer-------------

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("User already verified.")

        if not user.otp:
            raise serializers.ValidationError("No OTP found for this user. Please request a new one.")

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        user.is_verified = True
        user.is_active = True
        user.otp = None
        user.save(update_fields=['is_verified', 'is_active', 'otp'])

        return {'user': user}


#---------- Login Serializer -----------

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_verified:
            raise serializers.ValidationError("User not verified via OTP")

        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")

        attrs['user'] = user
        return attrs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, VerifyOTPSerializer, LoginSerializer
from .models import CustomUser
from .utils import send_otp_email, get_tokens_for_user


# -------- Register (send OTP to email) ----------

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp_email(user)
            return Response({'msg': 'User created. OTP sent to email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------- Verify OTP ----------

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({"msg": "OTP verified successfully. You can now login."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------- Resend OTP ----------

class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_verified:
            return Response({"msg": "User already verified"}, status=status.HTTP_400_BAD_REQUEST)

        send_otp_email(user)
        return Response({"msg": "New OTP sent to your email"}, status=status.HTTP_200_OK)


# -------- Login (JWT generation) ----------

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                "msg": "Login successful",
                "tokens": tokens,
                "user_type": user.user_type,
                "email": user.email,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
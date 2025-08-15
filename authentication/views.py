from .models import CustomUser
from .serializers import RegisterSerializer, VerifyOTPSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . utils import get_tokens , get_tokens


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'OTP sent to phone number'}, status=201)
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens(user)
            return Response({"msg": "Otp Verified Successfully ", "tokens": tokens}, status=200)
        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            tokens = get_tokens(user)
            return Response({ "msg": "Login successful", "tokens": tokens} , status=200)

        return Response(serializer.errors, status=400)

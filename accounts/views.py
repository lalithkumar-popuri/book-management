from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, 
UserChangePasswordSerializer, SendResetPasswordEmailSerializer, UserPasswordResetSerializer)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self,request):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"message" : "Registration Successful","token" : token},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    def post(self,request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'message':'Login Successfull',"token" : token},status=status.HTTP_200_OK)
            else:
                return Response({'error':'username or password is not correct'})
            
class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
class UserChangePasswordView(APIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = UserChangePasswordSerializer(data = request.data,context = {"user" : request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"message" : "Password Changed Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendResetPasswordEmailView(APIView):
    serializer_class = SendResetPasswordEmailSerializer
    def post(self,request):
        serializer = SendResetPasswordEmailSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"message" : "password reset link sent to your mail"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    serializer_class = SendResetPasswordEmailSerializer
    def post(self,request,uid,token):
        serializer = UserPasswordResetSerializer(data = request.data, context = {'uid' : uid, 'token' : token})
        if serializer.is_valid(raise_exception=True):
            return Response({"message" : "Password Reset Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

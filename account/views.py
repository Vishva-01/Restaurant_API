from django.shortcuts import render
from .serializers import *

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class RegisterAPI(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.save()
            token=Token.objects.create(user=user)
            return Response({"message": "User Created"})
        return Response(serializer.errors, status=400)
    

class LoginAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(username = serializer.data['username'],password = serializer.data['password'])
            if user:
                token, create = Token.objects.get_or_create(user=user)
                return Response({"message": "Login Successful", 'token': str(token)})
            else:
                return Response({"message": "Login Failed"}, status=401)
        return Response(serializer.errors, status=400)
    
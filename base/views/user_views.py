import email
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User

 

from base.serializer import ProductSerializer , UserSerializer , UserSerializerWithToken

# Create your views here.

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k , v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def registerUser(request):
    print(request.data)
    try:
        data = request.data
        user = User.objects.create(
        first_name = data['name'],
        username = data['email'],
        email = data['email'],
        password = make_password(data['password'])        
    )
        print(user.first_name)
        serializer = UserSerializerWithToken(user , many = False)
        return Response(serializer.data)
    except Exception as e :
        print(e)
        message = {'detail' : 'this username already tocken'}
        return Response(message , status=status.HTTP_400_BAD_REQUEST )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserProfil(request):
    user = request.user
    serializ=UserSerializerWithToken(user , many=False)
    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email'] 
    if data ['password'] != '' :
        user.password = make_password(data['password'])

    user.save()

    return Response(serializ.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfil(request):
    user = request.user
    serializ=UserSerializer(user , many=False)
    return Response(serializ.data)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializ=UserSerializer(users , many=True)
    return Response(serializ.data)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUserById(request , pk ):
    user = User.objects.get(id = pk)
    serializ=UserSerializer(user , many=False)
    return Response(serializ.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUser(request , pk):
    user = User.objects.get(id = pk)
    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email'] 
    user.is_staff = data['isAdmin'] 
   
    user.save()
    serializ=UserSerializer(user , many=False)
    return Response(serializ.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteUser (request , pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('user was deleted')



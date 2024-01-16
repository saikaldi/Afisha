from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import AuthorizeValidateSerializer, RegistrationValidateSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework import status


# Create your views here.
# @api_view(['POST'])
# def register_api_view(request):
#     serializer = RegisterValidateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     username = serializer.validated_data.get('username')
#     password = serializer.validated_data.get('password')
#
#     User.objects.create_user(username=username, password=password)
#     # User.objects.create_user(username=username, password=password, is_active=False) hw yandex
#     return Response(status=201)
#
# @api_view(['POST'])
# def authorize_api_view(request):
#     serializer = AuthorizeValidateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     # username = serializer.validated_data.get('username')
#     # password = serializer.validated_data.get('password')
#
#     user = authenticate(**serializer.validated_data)
#     if user:
#         try:
#             token = Token.objects.get(user=user)
#         except Token.DoesNotExist:
#             token = Token.objects.create(user=user)
#             return Response(data={'key':token.key})
#     return Response(status=401, data={'error': 'User credential error'})





@api_view(['POST'])
def register_api_view(request):
    serializer = RegistrationValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')
    email = serializer.validated_data.get('email')

    random_code = serializer.create_random_code()

    user = User.objects.create_user(username=username, email=email, password=password, is_active=False)


    user.profile.random_code = random_code
    user.profile.save()



    return Response({'detail': 'Verification code sent to email.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def confirm_user_api_view(request):

    confirmation_code = request.data.get('confirmation_code')

    try:
        user = User.objects.get(profile__random_code=confirmation_code)
    except User.DoesNotExist:
        raise ValidationError('Invalid confirmation code.')


    user.is_active = True
    user.save()

    return Response({'detail': 'User successfully confirmed.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def authorize_api_view(request):
    serializer = AuthorizeValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user:
        return Response({'detail': 'Authorization successful.'}, status=status.HTTP_200_OK)
    return Response(status=401, data={'error': 'User credential error'})
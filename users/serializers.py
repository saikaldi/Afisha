from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
import random

class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegistrationValidateSerializer(UserValidateSerializer):
    email = serializers.EmailField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')

    def create_random_code(self):
        return str(random.randint(100000, 999999))
class AuthorizeValidateSerializer(UserValidateSerializer):
    def password(self, password):
        return password


# class RegisterValidateSerializer(UserValidateSerializer):
#
#
#     def validate_username(self, username):
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise ValidationError('User already exists!')

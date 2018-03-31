from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Interest


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all(),
                                                                                message='Username taken')])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(),
                                                                              message='Email taken')])
    password = serializers.CharField(write_only=True, min_length=8,
                                     error_messages={
                                         "blank": "Password cannot be empty.",
                                         "min_length": "Password too short."
                                                     })

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        read_only = ('id', 'date_joined',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'name', 'description', 'color', )

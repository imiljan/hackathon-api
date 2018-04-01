from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import Event
from .models import Interest


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all(),
                                                                                message='Username taken')])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(),
                                                                              message='Email taken')])
    password = serializers.CharField(write_only=True, min_length=6,
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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'body', 'img', 'address', 'hashtag', 'created_at', 'deleted_at',
                  'start_at', 'end_at', 'lat', 'long', 'interest_id')

    # def create(self, validated_data):
    #     event = Event(validated_data)
    #     event.interest = Interest.objects.get(pk=1)
    #     event.save()
    #     return event

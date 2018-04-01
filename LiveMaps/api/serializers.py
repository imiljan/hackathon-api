import time

import os
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from LiveMaps import settings
from api.models import Event, Vote
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


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))


class EventSerializer(serializers.ModelSerializer):
    created_at_ts = TimestampField(source='created_at')
    start_at_ts = TimestampField(source='start_at')
    end_at_ts = TimestampField(source='end_at')
    image = serializers.SerializerMethodField()
    interest = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'body', 'image', 'address', 'hashtag', 'created_at', 'deleted_at',
                  'start_at', 'end_at', 'lat', 'long', 'created_at_ts', 'start_at_ts', 'end_at_ts', 'interest', 'rating')

    def get_interest(self, event):
        return Interest.objects.get(pk=event.interest_id).name

    def get_image(self, event):
        return os.path.join("http://10.20.29.116:8888/", event.img.name)

    def get_rating(self, event):
        return Vote.objects.filter(event=event).aggregate(sum=Sum('sign'))


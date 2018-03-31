from django.contrib.auth.models import User
from api.serializers import UserSerializer
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



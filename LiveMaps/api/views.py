import datetime
from django.db.models import Q
from rest_framework.decorators import api_view

from api.serializers import EventSerializer, InterestSerializer, UserSerializer, CreateEventSerializer
from django.contrib.auth.models import User
from rest_framework import mixins, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from .models import Event, Interest


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InterestViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


class UserCreateView(CreateAPIView):
    model = User
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(User.objects.get(username=request.data['username']))
            token = jwt_encode_handler(payload)

            temp = {'success': True,
                    'message': 'Registered',
                    'token': token
                    }

            return Response(temp, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class EventList(viewsets.ReadOnlyModelViewSet):
#     serializer_class = EventSerializer
#     queryset = Event.objects.all()


@api_view(['GET'])
def event_list(request):
    if request.method == "GET":
        if request.GET.get('interests'):
            interests = request.GET['interests']
            interests = interests.split(',')
            inter = [int(i) for i in interests]
            events = Event.objects.filter(Q(end_at__gt=datetime.datetime.now()), Q(interest_id__in=inter)).all()
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        events = Event.objects.filter(end_at__gt=datetime.datetime.now()).all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventCreateView(CreateAPIView):
    model = Event
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = CreateEventSerializer


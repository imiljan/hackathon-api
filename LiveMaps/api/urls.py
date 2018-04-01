from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api.views import EventList, EventCreateView
from .views import UserViewSet, InterestViewSet, UserCreateView

router = DefaultRouter()
router.register(r'users', viewset=UserViewSet)
router.register(r'interests', viewset=InterestViewSet)
router.register(r'events', viewset=EventList)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/register/', UserCreateView.as_view()),
    url(r'^event/', EventCreateView.as_view()),
]
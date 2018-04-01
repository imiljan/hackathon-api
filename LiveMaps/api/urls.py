from api.views import EventCreateView, event_detail
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import InterestViewSet, UserCreateView, UserViewSet, event_list

router = DefaultRouter()
router.register(r'users', viewset=UserViewSet)
router.register(r'interests', viewset=InterestViewSet)
# router.register(r'events', viewset=EventList)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/register/', UserCreateView.as_view()),
    url(r'^event/', EventCreateView.as_view()),
    url(r'^events/$', event_list),
    url(r'^events/(?P<pk>[0-9]+)/$', event_detail),
]

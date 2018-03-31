from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, InterestViewSet, UserCreateView

router = DefaultRouter()
router.register(r'users', viewset=UserViewSet)
router.register(r'interests', viewset=InterestViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/register/', UserCreateView.as_view())
]
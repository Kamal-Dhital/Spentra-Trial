from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import ProfileViewSet

router = DefaultRouter()
router.register(r'', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
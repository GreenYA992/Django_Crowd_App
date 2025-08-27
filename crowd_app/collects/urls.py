# noinspection PyUnresolvedReferences
from django.urls import path, include
# noinspection PyUnresolvedReferences
from rest_framework.routers import DefaultRouter
from .views import CollectViewSet

router = DefaultRouter()
router.register(r'', CollectViewSet, basename='collect')

urlpatterns = [
    path('', include(router.urls)),
]
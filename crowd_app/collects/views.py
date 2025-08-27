# noinspection PyUnresolvedReferences
from rest_framework import viewsets, status, permissions
# noinspection PyUnresolvedReferences
from rest_framework.decorators import action
# noinspection PyUnresolvedReferences
from rest_framework.response import Response
# noinspection PyUnresolvedReferences
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# noinspection PyUnresolvedReferences
from django.utils.decorators import method_decorator
# noinspection PyUnresolvedReferences
from django.views.decorators.cache import cache_page
# noinspection PyUnresolvedReferences
from django.views.decorators.vary import vary_on_cookie
from .models import Collect
from .serializers import CollectSerializer, CollectDetailSerializer
# noinspection PyUnresolvedReferences
from .tasks import send_collect_created_email
# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model


class CollectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]  # Для начала разрешим всем

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CollectDetailSerializer
        return CollectSerializer

    def get_queryset(self):
        queryset = Collect.objects.all()
        occasion = self.request.query_params.get('occasion')
        if occasion:
            queryset = queryset.filter(occasion=occasion)
        return queryset

    def perform_create(self, serializer):
        # Для тестирования без аутентификации
        User = get_user_model()
        first_user = User.objects.first()
        serializer.save(author=first_user)

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

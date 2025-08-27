# noinspection PyUnresolvedReferences
from rest_framework import serializers
from .models import Collect, Occasion
# noinspection PyUnresolvedReferences
from payments.models import Payment
# noinspection PyUnresolvedReferences
from payments.serializers import PaymentSerializer
# noinspection PyUnresolvedReferences
from django.utils import timezone

class CollectSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    payments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collect
        fields = [
            'id', 'author', 'author_name', 'title', 'occasion', 'description',
            'target_amount', 'current_amount', 'cover_image', 'end_datetime',
            'created_at', 'is_active', 'progress_percentage', 'payments_count'
        ]
        read_only_fields = ['author', 'current_amount', 'created_at']

    def validate_end_datetime(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                'Дата завершения должна быть в будущем'
            )
        return value

class CollectDetailSerializer(CollectSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta(CollectSerializer.Meta):
        fields = CollectSerializer.Meta.fields + ['payments']
# noinspection PyUnresolvedReferences
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    collect_title = serializers.CharField(source='collect.title', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_name', 'collect', 'collect_title',
            'amount', 'comment', 'is_anonymous', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Сумма платежа должна быть положительной'
            )
        return value
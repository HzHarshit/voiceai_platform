from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'description', 'status', 'voice_script',
            'target_audience', 'scheduled_start', 'scheduled_end',
            'created_by', 'created_by_username', 'tenant', 'tenant_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 'tenant')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['tenant'] = self.context['request'].user.tenant
        return super().create(validated_data)

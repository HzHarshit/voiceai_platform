from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Campaign
from .serializers import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        # Filter campaigns by the current user's tenant
        return Campaign.objects.filter(tenant=self.request.user.tenant)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        campaign = self.get_object()
        if campaign.status == 'draft':
            campaign.status = 'active'
            campaign.save()
            serializer = self.get_serializer(campaign)
            return Response(serializer.data)
        return Response({'error': 'Campaign can only be activated from draft status'},
                       status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        campaign = self.get_object()
        if campaign.status == 'active':
            campaign.status = 'paused'
            campaign.save()
            serializer = self.get_serializer(campaign)
            return Response(serializer.data)
        return Response({'error': 'Campaign can only be paused from active status'},
                       status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        campaign = self.get_object()
        if campaign.status in ['active', 'paused']:
            campaign.status = 'completed'
            campaign.save()
            serializer = self.get_serializer(campaign)
            return Response(serializer.data)
        return Response({'error': 'Campaign can only be completed from active or paused status'},
                       status=status.HTTP_400_BAD_REQUEST)

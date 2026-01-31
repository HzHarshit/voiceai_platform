from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Call
from .serializers import CallSerializer
from voice_providers.services import VoiceProviderService


class CallViewSet(viewsets.ModelViewSet):
    serializer_class = CallSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'campaign', 'provider_name']
    search_fields = ['phone_number', 'message']
    ordering_fields = ['created_at', 'completed_at', 'duration', 'cost']
    ordering = ['-created_at']

    def get_queryset(self):
        # Filter calls by the current user's tenant
        return Call.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Set tenant and created_by automatically
        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user
        )

    @action(detail=True, methods=['post'])
    def initiate(self, request, pk=None):
        call = self.get_object()
        if call.status != 'pending':
            return Response({'error': 'Call can only be initiated from pending status'},
                           status=status.HTTP_400_BAD_REQUEST)

        try:
            provider_service = VoiceProviderService()
            result = provider_service.make_call(
                phone_number=call.phone_number,
                message=call.message,
                tenant=call.tenant
            )

            call.status = 'initiated'
            call.provider_call_id = result.get('id')
            call.provider_name = result.get('provider', 'mock')
            call.metadata = result
            call.save()

            serializer = self.get_serializer(call)
            return Response(serializer.data)

        except Exception as e:
            call.status = 'failed'
            call.metadata = {'error': str(e)}
            call.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def hangup(self, request, pk=None):
        call = self.get_object()
        if call.status not in ['initiated', 'in_progress']:
            return Response({'error': 'Call can only be hung up when initiated or in progress'},
                           status=status.HTTP_400_BAD_REQUEST)

        try:
            provider_service = VoiceProviderService()
            success = provider_service.hangup_call(call.provider_call_id, call.tenant)

            if success:
                call.status = 'completed'
                call.save()
                serializer = self.get_serializer(call)
                return Response(serializer.data)
            else:
                return Response({'error': 'Failed to hang up call'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        total_calls = queryset.count()
        completed_calls = queryset.filter(status='completed').count()
        failed_calls = queryset.filter(status='failed').count()
        total_duration = queryset.filter(status='completed').aggregate(
            total=models.Sum('duration')
        )['total'] or 0
        total_cost = queryset.aggregate(total=models.Sum('cost'))['total'] or 0

        return Response({
            'total_calls': total_calls,
            'completed_calls': completed_calls,
            'failed_calls': failed_calls,
            'success_rate': (completed_calls / total_calls * 100) if total_calls > 0 else 0,
            'total_duration': total_duration,
            'total_cost': total_cost,
        })

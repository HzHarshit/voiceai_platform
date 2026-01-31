from celery import shared_task
from django.utils import timezone
from .models import Call
from voice_providers.services import VoiceProviderService


@shared_task
def process_call(call_id):
    """Process a voice call asynchronously."""
    try:
        call = Call.objects.get(id=call_id)
        provider_service = VoiceProviderService()

        # Make the call
        result = provider_service.make_call(
            phone_number=call.phone_number,
            message=call.message,
            tenant=call.tenant
        )

        # Update call with provider information
        call.status = 'initiated'
        call.provider_call_id = result.get('id')
        call.provider_name = result.get('provider', 'mock')
        call.metadata = result
        call.save()

        # Schedule status check
        check_call_status.apply_async((call_id,), countdown=30)

    except Call.DoesNotExist:
        pass
    except Exception as e:
        call.status = 'failed'
        call.metadata = {'error': str(e)}
        call.save()


@shared_task
def check_call_status(call_id):
    """Check the status of an ongoing call."""
    try:
        call = Call.objects.get(id=call_id)
        if call.status in ['initiated', 'in_progress']:
            provider_service = VoiceProviderService()
            status_info = provider_service.get_call_status(call.provider_call_id, call.tenant)

            call.status = status_info.get('status', call.status)
            call.duration = status_info.get('duration', call.duration)
            call.cost = status_info.get('cost', call.cost)
            call.metadata.update(status_info)

            if call.status == 'completed':
                call.completed_at = timezone.now()

            call.save()

            # Schedule another check if call is still active
            if call.status in ['initiated', 'in_progress']:
                check_call_status.apply_async((call_id,), countdown=30)

    except Call.DoesNotExist:
        pass
    except Exception as e:
        call.status = 'failed'
        call.metadata = {'error': str(e)}
        call.save()


@shared_task
def bulk_process_campaign_calls(campaign_id):
    """Process all pending calls for a campaign."""
    from campaigns.models import Campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
        pending_calls = Call.objects.filter(
            campaign=campaign,
            status='pending'
        )

        for call in pending_calls:
            process_call.delay(call.id)

    except Campaign.DoesNotExist:
        pass

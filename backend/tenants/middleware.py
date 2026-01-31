from django.db import connection
from django.http import Http404
from .models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract tenant from subdomain or header
        host = request.get_host().split(':')[0]  # Remove port if present
        subdomain = host.split('.')[0] if '.' in host else None

        if subdomain:
            try:
                tenant = Tenant.objects.get(domain=subdomain)
                request.tenant = tenant
                # Set tenant schema for PostgreSQL (if using schema-based multi-tenancy)
                # connection.set_schema(tenant.schema_name)
            except Tenant.DoesNotExist:
                raise Http404("Tenant not found")
        else:
            # For development, you might want to set a default tenant
            # request.tenant = Tenant.objects.first()
            pass

        response = self.get_response(request)
        return response

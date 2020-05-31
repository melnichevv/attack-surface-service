from django.conf import settings
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from atss.apps.vm.models import VirtualMachine


class StatsView(APIView):
    @swagger_auto_schema(
        auto_schema=SwaggerAutoSchema,
        responses={
            "200": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "vm_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "request_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "average_request_time": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                },
            ),
            "404": "Not Found",
        },
        security=None,
        operation_id="stats",
        operation_description="Get service statistics",
    )
    def get(self, request: Request) -> Response:
        """Return list of virtual machine IDs that can potentially attack particular virtual machine."""
        request_count, avg_request_time = cache.get(
            settings.STATS_CACHE_KEY, {"request_count": 0, "avg_request_time": 0}
        ).values()
        return Response(
            {
                "vm_count": VirtualMachine.objects.count(),
                "request_count": request_count,
                "average_request_time": avg_request_time,
            }
        )

from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from atss.apps.vm.models import VirtualMachine
from atss.apps.vm.queries import get_possible_attackers


class AttackView(APIView):
    @swagger_auto_schema(
        auto_schema=SwaggerAutoSchema,
        responses={
            "200": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            "404": "Not Found",
        },
        security=None,
        operation_id="attack_vm",
        operation_description="Get list of the virtual machine ids that can potentially attack particular VM.",
        manual_parameters=[openapi.Parameter("vm_id", openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)],
    )
    def get(self, request: Request) -> Response:
        """Return list of virtual machine IDs that can potentially attack particular virtual machine."""
        vm = get_object_or_404(VirtualMachine, vm_id=request.GET.get("vm_id"))
        possible_attackers = get_possible_attackers(vm)
        return Response(list(possible_attackers.values_list("vm_id", flat=True)))

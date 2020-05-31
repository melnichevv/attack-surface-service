from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def get_swagger_with_version(version):
    return get_schema_view(
        openapi.Info(
            title="Attack surface service API",
            default_version=version,
            contact=openapi.Contact(email="melnichevv@gmail.com"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

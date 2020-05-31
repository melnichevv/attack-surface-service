from django.conf import settings
from django.urls import include, path

from atss.api.utils.swagger import get_swagger_with_version

app_name = "v1"


urlpatterns = [path("", include("atss.api.versions.v1.vm.urls"))]

if settings.DRF_YASG:
    schema_view = get_swagger_with_version(app_name)

    urlpatterns += [path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui")]

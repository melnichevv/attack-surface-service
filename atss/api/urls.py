"""
Main API url module

Contains the roots of all API versions (active and deprecated ones).

While all API versions are imported here, they should also import each other in their respective 'urls.py' file to
allow the access to the endpoint in older versions from the newer versions.

Every new API version should be added here and to LATEST_VERSION and ALLOWED_VERSIONS in settings/common.py
"""

from django.urls import include, path

app_name = "api"

urlpatterns = [path("v1/", include("atss.api.versions.v1.urls", namespace="v1"))]

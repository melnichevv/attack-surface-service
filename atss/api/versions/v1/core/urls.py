from django.urls import path

from .views import StatsView

app_name = "core_v1"

urlpatterns = [path("stats", StatsView.as_view(), name="stats")]

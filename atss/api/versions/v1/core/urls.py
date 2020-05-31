from django.urls import path

from .views import StatsView

app_name = "vm_v1"

urlpatterns = [path("stats/", StatsView.as_view(), name="stats")]

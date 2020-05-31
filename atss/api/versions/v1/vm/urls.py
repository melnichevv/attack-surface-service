from django.urls import path

from .views import AttackView

app_name = "vm_v1"

urlpatterns = [path("attack/", AttackView.as_view(), name="attack_vm")]

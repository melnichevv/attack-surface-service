from django.urls import path

from atss.api.versions.v1.vm.views.attack import AttackView

app_name = "vm_v1"

urlpatterns = [path("attack", AttackView.as_view(), name="users")]

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _lazy


class VirtualMachine(models.Model):
    vm_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    tags = ArrayField(models.CharField(max_length=50), default=list, help_text=_lazy("List of tags"))

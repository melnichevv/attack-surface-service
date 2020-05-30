from django.db import models


class VirtualMachine(models.Model):
    vm_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    tags = models.ManyToManyField("vm.Tag", related_name="virtual_machines")

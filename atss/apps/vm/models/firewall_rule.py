from django.db import models


class FirewallRule(models.Model):
    fw_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    source_tag = models.ForeignKey("vm.Tag", related_name="source_rules", on_delete=models.CASCADE)
    dest_tag = models.ForeignKey("vm.Tag", related_name="target_rules", on_delete=models.CASCADE)

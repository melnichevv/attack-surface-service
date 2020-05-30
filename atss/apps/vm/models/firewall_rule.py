from django.db import models


class FirewallRule(models.Model):
    fw_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    source_tag = models.CharField(max_length=100)
    dest_tag = models.CharField(max_length=100)

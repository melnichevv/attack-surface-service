import json
import logging

from django.db import transaction

from atss.apps.vm.models.firewall_rule import FirewallRule
from atss.apps.vm.models.tag import Tag
from atss.apps.vm.models.virtual_machine import VirtualMachine

logger = logging.getLogger(__name__)


def get_data_from_file(filename):
    try:
        with open(filename, "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        logger.error(
            f"File {filename} not found. Please make sure that this file exists and try running this command again."
        )
        return {}


@transaction.atomic
def load_data_from_file(filename="data_inputs/input-0.json"):
    file_data = get_data_from_file(filename)
    if not file_data:
        return {}
    tags = [tag for vm in file_data["vms"] for tag in vm["tags"]]
    tags.extend([tag for fw_rule in file_data["fw_rules"] for tag in [fw_rule["source_tag"], fw_rule["dest_tag"]]])
    tags = set(tags)
    tag_objects = []
    for tag_name in tags:
        tag_objects.append(Tag(name=tag_name))
    tag_objects = Tag.objects.bulk_create(tag_objects)
    tags_map = {tag.name: tag for tag in tag_objects}

    #  create tags
    vm_tags_map = {}
    vm_objects = []
    for vm_data in file_data["vms"]:
        vm = VirtualMachine(vm_id=vm_data["vm_id"], name=vm_data["name"])
        vm_objects.append(vm)
        vm_tags_map[vm_data["vm_id"]] = {"obj": vm, "tags": [tags_map[name] for name in vm_data["tags"]]}

    vm_objects = VirtualMachine.objects.bulk_create(vm_objects)
    for vm in vm_objects:
        vm.tags.set(vm_tags_map[vm.vm_id]["tags"])
        vm.save()

    fw_rules = FirewallRule.objects.bulk_create(
        [
            FirewallRule(
                fw_id=fw_rule_data["fw_id"],
                source_tag=tags_map[fw_rule_data["source_tag"]],
                dest_tag=tags_map[fw_rule_data["dest_tag"]],
            )
            for fw_rule_data in file_data["fw_rules"]
        ]
    )

    return {"vm": len(vm_objects), "tags": len(tag_objects), "fw_rules": len(fw_rules)}

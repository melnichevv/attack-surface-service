import json
import logging
from json import JSONDecodeError
from typing import Dict, Optional

from django.db import transaction

from atss.apps.vm.models.firewall_rule import FirewallRule
from atss.apps.vm.models.virtual_machine import VirtualMachine

logger = logging.getLogger(__name__)


def get_data_from_file(file: str):
    try:
        with open(file, "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        logger.error(
            f"File {file} not found. Please make sure that this file exists and try running this command again."
        )
    except JSONDecodeError as e:
        logger.error(f"An error occurred during parsing JSON file: {e}")
    return {}


@transaction.atomic
def load_data_from_file(file: Optional[str] = "data_inputs/input-0.json") -> Dict[str, int]:
    """Create VirtualMachine and FirewallRule objects based on data in `file`."""
    file_data = get_data_from_file(file)
    if not file_data or not isinstance(file_data, dict):
        return {}

    vms = VirtualMachine.objects.bulk_create(
        [
            VirtualMachine(vm_id=vm_data["vm_id"], name=vm_data["name"], tags=vm_data["tags"])
            for vm_data in file_data["vms"]
        ]
    )

    fw_rules = FirewallRule.objects.bulk_create(
        [
            FirewallRule(
                fw_id=fw_rule_data["fw_id"], source_tag=fw_rule_data["source_tag"], dest_tag=fw_rule_data["dest_tag"]
            )
            for fw_rule_data in file_data["fw_rules"]
        ]
    )

    return {"vm": len(vms), "fw_rules": len(fw_rules)}

from django.db.models import QuerySet

from atss.apps.vm.models import FirewallRule, VirtualMachine


def get_possible_attackers(vm: VirtualMachine) -> QuerySet:
    """
    Return QuerySet of possible attackers VMs based on firewall rules and list of tags attached to target VM.

    This implementation doesn't work with recursive firewall rules.
    """
    source_tags = FirewallRule.objects.filter(dest_tag__in=vm.tags).values_list("source_tag", flat=True)
    attackers = VirtualMachine.objects.filter(tags__overlap=list(source_tags)).exclude(vm_id=vm.vm_id)
    return attackers

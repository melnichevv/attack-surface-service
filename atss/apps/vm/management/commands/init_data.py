import logging

from django.core.cache import cache
from django.core.management import BaseCommand

from atss.apps.vm.models import FirewallRule, VirtualMachine
from atss.apps.vm.utils.virtual_machine import load_data_from_file

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load VirtualMachine and FirewallRules data from JSON file into DB."

    def add_arguments(self, parser):
        parser.add_argument("--file_path", type=str)

    def handle(self, *args, **options):
        try:
            VirtualMachine.objects.all().delete()
            FirewallRule.objects.all().delete()
            load_data_from_file(options["file_path"])
            cache.clear()
        except Exception as e:
            logger.error(f"Something went wrong. {e}")

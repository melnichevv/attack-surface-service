import logging

from django.core.management import BaseCommand

from atss.apps.vm.utils.virtual_machine import load_data_from_file

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load VirtualMachine and FirewallRules data from JSON file into DB."

    def add_arguments(self, parser):
        parser.add_argument("--file_path", type=str)

    def handle(self, *args, **options):
        try:
            load_data_from_file(options["file_path"])
        except Exception as e:
            logger.error(f"Something went wrong. {e}")

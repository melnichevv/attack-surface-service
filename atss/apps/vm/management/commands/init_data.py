import logging

from django.core.management import BaseCommand

from atss.apps.vm.utils.virtual_machine import load_data_from_file

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads vm and firewall rules data from JSON file into DB."

    def add_arguments(self, parser):
        parser.add_argument("--file_path", type=str)

    def handle(self, *args, **options):
        load_data_from_file(options["file_path"])

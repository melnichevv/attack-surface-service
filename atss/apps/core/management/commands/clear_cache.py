import logging

from django.core.cache import cache
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Clear site-wide cache."""

    def handle(self, *args, **kwargs):
        cache.clear()
        logger.info("Cache has been cleared!")

from time import time

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse


class StatsMiddleware:
    """Simple middleware for request time calculation and storing it in cache."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.process_request(request)

    def process_request(self, request):
        start = time()
        response = self.get_response(request)
        total_time = time() - start
        request_count, avg_request_time = cache.get(
            settings.STATS_CACHE_KEY, {"request_count": 0, "avg_request_time": 0}
        ).values()
        cache.set(
            settings.STATS_CACHE_KEY,
            {
                "request_count": request_count + 1,
                "avg_time": (request_count * avg_request_time + total_time) / (request_count + 1),
            },
        )

        return response

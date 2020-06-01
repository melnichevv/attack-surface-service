from unittest import mock

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

TEST_MODULE = "atss.api.versions.v1.core.views.stats"
BASE_API_V1_PATH = "/api/v1"


@pytest.mark.django_db
class TestStatsView:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.url = f"{BASE_API_V1_PATH}/stats"
        self.api_client = APIClient()

    @pytest.mark.parametrize("method,status_code", [("get", 200), ("put", 405), ("patch", 405), ("delete", 405)])
    @mock.patch(f"{TEST_MODULE}.StatsView.get")
    def test_accessible_methods(self, mock_get, method, status_code):
        mock_get.return_value = Response()
        response = getattr(self.api_client, method)(self.url)
        assert response.status_code == status_code

    @mock.patch(f"{TEST_MODULE}.cache.get", return_value={"request_count": 178, "avg_request_time": 0.0031728462})
    @mock.patch(f"{TEST_MODULE}.VirtualMachine.objects.count", return_value=13)
    def test_get_return_value(self, mock_count, mock_cache):
        response = self.api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == {"vm_count": 13, "request_count": 178, "average_request_time": 0.0031728462}

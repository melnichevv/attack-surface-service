from unittest import mock

import pytest
from rest_framework.test import APIClient

from atss.apps.vm.models import VirtualMachine

TEST_MODULE = "atss.api.versions.v1.vm.views.attack"
BASE_API_V1_PATH = "/api/v1"


@pytest.mark.django_db
class TestAttackView:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.url = f"{BASE_API_V1_PATH}/attack"
        self.api_client = APIClient()

    @mock.patch(f"{TEST_MODULE}.get_object_or_404")
    @pytest.mark.parametrize("method,status_code", [("get", 200), ("put", 405), ("patch", 405), ("delete", 405)])
    def test_accessible_methods(self, mock_get_object_or_404, method, status_code):
        mock_get_object_or_404.return_value = mock.MagicMock(spec=VirtualMachine, vm_id="vm-100000")
        response = getattr(self.api_client, method)(f"{self.url}?vm_id=vm-111111")
        assert response.status_code == status_code

    @mock.patch(f"{TEST_MODULE}.get_object_or_404")
    @mock.patch(f"{TEST_MODULE}.get_possible_attackers")
    def test_get_is_accessible(self, mock_get_possible_attackers, mock_get_object_or_404):
        mock_get_object_or_404.return_value = mock.MagicMock(spec=VirtualMachine, vm_id="vm-100000")
        assert mock_get_possible_attackers.called_once()
        response = self.api_client.get(f"{self.url}?vm_id=vm-111111")
        assert response.status_code == 200

    def test_throws_404(self):
        vm_id = "vm-111111"
        assert not VirtualMachine.objects.filter(vm_id=vm_id).exists()
        response = self.api_client.get(f"{BASE_API_V1_PATH}/{vm_id}")
        assert response.status_code == 404

    @mock.patch(f"{TEST_MODULE}.get_object_or_404")
    @mock.patch(f"{TEST_MODULE}.get_possible_attackers")
    def test_get_return_value(self, mock_get_possible_attackers, mock_get_object_or_404):
        mock_get_object_or_404.return_value = mock.MagicMock(spec=VirtualMachine, vm_id="vm-100000")
        mock_get_possible_attackers.return_value = mock.Mock(
            values_list=mock.Mock(return_value=["vm-123456", "vm-123457", "vm-123458"])
        )
        response = self.api_client.get(f"{self.url}?vm_id=vm-111111")
        assert response.status_code == 200
        assert response.data == ["vm-123456", "vm-123457", "vm-123458"]

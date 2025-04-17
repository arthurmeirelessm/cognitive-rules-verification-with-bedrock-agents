import pytest
from unittest.mock import AsyncMock, patch
from src.services.run_test_service import RunTestService  # Importe corretamente seu serviço

@pytest.mark.asyncio
async def test_create_item_service_success():
    service = RunTestService()

    # Mocka o verify_jwt para sempre retornar True
    service.jwt_auth = AsyncMock()
    service.jwt_auth.verify_jwt.return_value = True

    # Mocka o create_item para retornar True (simulando criação bem-sucedida)
    service.dynamo_client = AsyncMock()
    service.dynamo_client.create_item.return_value = True

    response, status = await service.create_item_service("fake_token", "12345678900", "email@test.com", "User Test", "999999999")

    assert response == "Usuario criado com sucesso!"
    assert status == 200


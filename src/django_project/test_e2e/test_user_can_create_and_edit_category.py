import pytest
from rest_framework.test import APIClient
import json


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self, api_client: APIClient) -> None:
        # Acessa listagem e verifica que não tem nenhuma categoria criada
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}

        # Cria uma categoria
        create_response = api_client.post(
            "/api/categories/",
            {
                "name": "Movie",
                "description": "Movie description",
            },
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        # Verifica que categoria criada aparece na listagem
        assert api_client.get("/api/categories/").data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ]
        }

        # Edita categoria criada
        edit_response = api_client.put(
            f"/api/categories/{created_category_id}/",
            data=json.dumps({
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            }),
            content_type="application/json",
        )
        assert edit_response.status_code == 204

        # Verifica que categoria editada aparece na listagem
        api_client.get("/api/categories/").data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True,
                }
            ]
        }

    def test_patch_update_name_only(self, api_client: APIClient) -> None:
        # Cria categoria
        create_response = api_client.post(
            "/api/categories/",
            {
                "name": "Original Name",
                "description": "Original description",
                "is_active": True,
            },
        )
        assert create_response.status_code == 201
        category_id = create_response.data["id"]

        # PATCH apenas o nome
        patch_response = api_client.patch(
            f"/api/categories/{category_id}/",
            data=json.dumps({"name": "Updated Name"}),
            content_type="application/json",
        )
        assert patch_response.status_code == 204

        # Verifica que só o nome mudou
        list_response = api_client.get("/api/categories/")
        data = list_response.data["data"][0]
        assert data["id"] == category_id
        assert data["name"] == "Updated Name"
        assert data["description"] == "Original description"
        assert data["is_active"] is True

    def test_patch_update_description_only(self, api_client: APIClient) -> None:
        # Cria categoria
        create_response = api_client.post(
            "/api/categories/",
            {
                "name": "Original Name",
                "description": "Original description",
                "is_active": True,
            },
        )
        assert create_response.status_code == 201
        category_id = create_response.data["id"]

        # PATCH apenas a descrição
        patch_response = api_client.patch(
            f"/api/categories/{category_id}/",
            data=json.dumps({"description": "Updated description"}),
            content_type="application/json",
        )
        assert patch_response.status_code == 204

        # Verifica que só a descrição mudou
        list_response = api_client.get("/api/categories/")
        data = list_response.data["data"][0]
        assert data["id"] == category_id
        assert data["name"] == "Original Name"
        assert data["description"] == "Updated description"
        assert data["is_active"] is True

    def test_patch_update_is_active_only(self, api_client: APIClient) -> None:
        # Cria categoria
        create_response = api_client.post(
            "/api/categories/",
            {
                "name": "Original Name",
                "description": "Original description",
                "is_active": True,
            },
        )
        assert create_response.status_code == 201
        category_id = create_response.data["id"]

        # PATCH apenas o is_active
        patch_response = api_client.patch(
            f"/api/categories/{category_id}/",
            data=json.dumps({"is_active": False}),
            content_type="application/json",
        )
        assert patch_response.status_code == 204

        # Verifica que só o is_active mudou
        list_response = api_client.get("/api/categories/")
        data = list_response.data["data"][0]
        assert data["id"] == category_id
        assert data["name"] == "Original Name"
        assert data["description"] == "Original description"
        assert data["is_active"] is False

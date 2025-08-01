import pytest
from rest_framework import status
from rest_framework.test import APIClient
from uuid import uuid4

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def cast_member_actor():
    return CastMember(
        name="John Doe",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def cast_member_director():
    return CastMember(
        name="Jane Smith",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        cast_member_actor: CastMember,
        cast_member_director: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(cast_member_actor)
        cast_member_repository.save(cast_member_director)

        url = "/api/cast-members/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "data" in response.data
        assert "meta" in response.data
        
        # Check meta information
        assert response.data["meta"]["current_page"] == 1
        assert response.data["meta"]["per_page"] == 2
        assert response.data["meta"]["total"] == 2
        
        # Check that both cast members are in the response
        cast_member_ids = [cm["id"] for cm in response.data["data"]]
        assert str(cast_member_actor.id) in cast_member_ids
        assert str(cast_member_director.id) in cast_member_ids


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        url = "/api/cast-members/"
        data = {
            "name": "New Actor",
            "type": "ACTOR",
        }
        response = APIClient().post(url, data=data, content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

        saved_cast_member = cast_member_repository.get_by_id(response.data["id"])
        assert saved_cast_member is not None
        assert saved_cast_member.name == "New Actor"
        assert saved_cast_member.type == CastMemberType.ACTOR

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = "/api/cast-members/"
        data = {
            "name": "",
            "type": "INVALID_TYPE",
        }
        response = APIClient().post(url, data=data, content_type="application/json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST 
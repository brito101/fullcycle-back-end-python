import pytest
from uuid import uuid4

from src.core.cast_member.application.use_cases import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input_data = CreateCastMember.Input(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        # Act
        output = use_case.execute(input_data)

        # Assert
        assert output.id is not None
        saved_cast_member = repository.get_by_id(output.id)
        assert saved_cast_member is not None
        assert saved_cast_member.name == "John Doe"
        assert saved_cast_member.type == CastMemberType.ACTOR

    def test_create_cast_member_with_director_type(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input_data = CreateCastMember.Input(
            name="Jane Doe",
            type=CastMemberType.DIRECTOR,
        )

        # Act
        output = use_case.execute(input_data)

        # Assert
        assert output.id is not None
        saved_cast_member = repository.get_by_id(output.id)
        assert saved_cast_member is not None
        assert saved_cast_member.name == "Jane Doe"
        assert saved_cast_member.type == CastMemberType.DIRECTOR

    def test_create_cast_member_with_empty_name_raises_error(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input_data = CreateCastMember.Input(
            name="",
            type=CastMemberType.ACTOR,
        )

        # Act & Assert
        with pytest.raises(InvalidCastMember, match="Name cannot be empty"):
            use_case.execute(input_data)

    def test_create_cast_member_with_invalid_type_raises_error(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input_data = CreateCastMember.Input(
            name="John Doe",
            type="INVALID_TYPE",  # type: ignore
        )

        # Act & Assert
        with pytest.raises(InvalidCastMember, match="Type must be a valid CastMemberType"):
            use_case.execute(input_data) 
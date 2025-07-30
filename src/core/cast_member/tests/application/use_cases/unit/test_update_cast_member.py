import pytest
from uuid import uuid4

from src.core.cast_member.application.use_cases import UpdateCastMember
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
    def test_update_cast_member_with_valid_data(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository.save(cast_member)
        
        use_case = UpdateCastMember(repository=repository)
        input_data = UpdateCastMember.Input(
            id=cast_member.id,
            name="Jane Doe",
            type=CastMemberType.DIRECTOR,
        )

        # Act
        output = use_case.execute(input_data)

        # Assert
        assert output.id == cast_member.id
        assert output.name == "Jane Doe"
        assert output.type == CastMemberType.DIRECTOR
        
        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member is not None
        assert updated_cast_member.name == "Jane Doe"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_update_cast_member_not_found_raises_error(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = UpdateCastMember(repository=repository)
        input_data = UpdateCastMember.Input(
            id=uuid4(),
            name="Jane Doe",
            type=CastMemberType.DIRECTOR,
        )

        # Act & Assert
        with pytest.raises(CastMemberNotFound, match="CastMember with id"):
            use_case.execute(input_data)

    def test_update_cast_member_with_empty_name_raises_error(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository.save(cast_member)
        
        use_case = UpdateCastMember(repository=repository)
        input_data = UpdateCastMember.Input(
            id=cast_member.id,
            name="",
            type=CastMemberType.ACTOR,
        )

        # Act & Assert
        with pytest.raises(InvalidCastMember, match="Name cannot be empty"):
            use_case.execute(input_data)

    def test_update_cast_member_with_invalid_type_raises_error(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository.save(cast_member)
        
        use_case = UpdateCastMember(repository=repository)
        input_data = UpdateCastMember.Input(
            id=cast_member.id,
            name="Jane Doe",
            type="INVALID_TYPE",  # type: ignore
        )

        # Act & Assert
        with pytest.raises(InvalidCastMember, match="Type must be a valid CastMemberType"):
            use_case.execute(input_data) 
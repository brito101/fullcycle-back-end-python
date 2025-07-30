import pytest
from uuid import uuid4

from src.core.cast_member.application.use_cases import DeleteCastMember
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member_with_valid_id(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository.save(cast_member)
        
        use_case = DeleteCastMember(repository=repository)
        input_data = DeleteCastMember.Input(id=cast_member.id)

        # Act
        use_case.execute(input_data)

        # Assert
        deleted_cast_member = repository.get_by_id(cast_member.id)
        assert deleted_cast_member is None

    def test_delete_cast_member_not_found_raises_error(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = DeleteCastMember(repository=repository)
        input_data = DeleteCastMember.Input(id=uuid4())

        # Act & Assert
        with pytest.raises(CastMemberNotFound, match="CastMember with id"):
            use_case.execute(input_data)

    def test_delete_cast_member_does_not_affect_others(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member1 = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member2 = CastMember(name="Jane Doe", type=CastMemberType.DIRECTOR)
        repository.save(cast_member1)
        repository.save(cast_member2)
        
        use_case = DeleteCastMember(repository=repository)
        input_data = DeleteCastMember.Input(id=cast_member1.id)

        # Act
        use_case.execute(input_data)

        # Assert
        deleted_cast_member = repository.get_by_id(cast_member1.id)
        assert deleted_cast_member is None
        
        remaining_cast_member = repository.get_by_id(cast_member2.id)
        assert remaining_cast_member is not None
        assert remaining_cast_member.name == "Jane Doe"
        assert remaining_cast_member.type == CastMemberType.DIRECTOR 
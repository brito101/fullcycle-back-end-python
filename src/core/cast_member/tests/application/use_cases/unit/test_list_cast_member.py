import pytest
from uuid import uuid4

from src.core.cast_member.application.use_cases.list_cast_member import (
    ListCastMember,
    ListCastMemberRequest,
    ListCastMemberResponse,
    CastMemberOutput,
)
from src.core._shared.application.use_cases.list_use_case import ListOutputMeta
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestListCastMember:
    def test_list_cast_members_when_empty(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=repository)
        input_data = ListCastMemberRequest()

        # Act
        output = use_case.execute(input_data)

        # Assert
        assert output == ListCastMemberResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=0,
            ),
        )

    def test_list_cast_members_with_data(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member1 = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member2 = CastMember(name="Jane Doe", type=CastMemberType.DIRECTOR)
        repository.save(cast_member1)
        repository.save(cast_member2)
        
        use_case = ListCastMember(repository=repository)
        input_data = ListCastMemberRequest()

        # Act
        output = use_case.execute(input_data)

        # Assert
        assert len(output.data) == 2
        assert output.meta == ListOutputMeta(
            current_page=1,
            per_page=2,
            total=2,
        )
        
        # Check that both cast members are in the response
        cast_member_ids = [cm.id for cm in output.data]
        assert cast_member1.id in cast_member_ids
        assert cast_member2.id in cast_member_ids
        
        # Check that the data contains the expected cast members
        for cast_member_output in output.data:
            if cast_member_output.id == cast_member1.id:
                assert cast_member_output.name == "John Doe"
                assert cast_member_output.type == "ACTOR"
            elif cast_member_output.id == cast_member2.id:
                assert cast_member_output.name == "Jane Doe"
                assert cast_member_output.type == "DIRECTOR"

    def test_list_cast_members_returns_copy(self):
        # Arrange
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        repository.save(cast_member)
        
        use_case = ListCastMember(repository=repository)
        input_data = ListCastMemberRequest()

        # Act
        output1 = use_case.execute(input_data)
        output2 = use_case.execute(input_data)

        # Assert
        assert output1.data is not output2.data  # Should be different objects
        assert output1.data == output2.data  # But same content 
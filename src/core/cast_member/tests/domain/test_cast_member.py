import pytest
from uuid import uuid4
import dataclasses

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_create_cast_member_with_valid_data(self):
        # Arrange
        name = "John Doe"
        type_ = CastMemberType.ACTOR

        # Act
        cast_member = CastMember(name=name, type=type_)

        # Assert
        assert cast_member.name == name
        assert cast_member.type == type_
        assert cast_member.id is not None

    def test_create_cast_member_with_director_type(self):
        # Arrange
        name = "Jane Doe"
        type_ = CastMemberType.DIRECTOR

        # Act
        cast_member = CastMember(name=name, type=type_)

        # Assert
        assert cast_member.name == name
        assert cast_member.type == type_

    def test_create_cast_member_with_custom_id(self):
        # Arrange
        custom_id = uuid4()
        name = "John Doe"
        type_ = CastMemberType.ACTOR

        # Act
        cast_member = CastMember(id=custom_id, name=name, type=type_)

        # Assert
        assert cast_member.id == custom_id
        assert cast_member.name == name
        assert cast_member.type == type_

    def test_create_cast_member_with_empty_name_raises_error(self):
        # Arrange
        name = ""
        type_ = CastMemberType.ACTOR

        # Act & Assert
        with pytest.raises(ValueError, match="Name cannot be empty"):
            CastMember(name=name, type=type_)

    def test_create_cast_member_with_invalid_type_raises_error(self):
        # Arrange
        name = "John Doe"
        type_ = "INVALID_TYPE"

        # Act & Assert
        with pytest.raises(ValueError, match="Type must be a valid CastMemberType"):
            CastMember(name=name, type=type_)

    def test_cast_member_is_immutable(self):
        # Arrange
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        original_name = cast_member.name

        # Act & Assert
        with pytest.raises(dataclasses.FrozenInstanceError):
            cast_member.name = "Jane Doe"

    def test_cast_member_equality(self):
        # Arrange
        id_ = uuid4()
        cast_member1 = CastMember(id=id_, name="John Doe", type=CastMemberType.ACTOR)
        cast_member2 = CastMember(id=id_, name="John Doe", type=CastMemberType.ACTOR)

        # Assert
        assert cast_member1 == cast_member2

    def test_cast_member_inequality(self):
        # Arrange
        cast_member1 = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member2 = CastMember(name="Jane Doe", type=CastMemberType.DIRECTOR)

        # Assert
        assert cast_member1 != cast_member2 
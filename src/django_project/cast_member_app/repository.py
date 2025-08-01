from uuid import UUID
from typing import List

from django.core.exceptions import ObjectDoesNotExist

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepository):
    def save(self, cast_member: CastMember) -> None:
        cast_member_model = CastMemberModel(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type.value,
        )
        cast_member_model.save()

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_model = CastMemberModel.objects.get(id=id)
            return CastMember(
                id=cast_member_model.id,
                name=cast_member_model.name,
                type=CastMemberType(cast_member_model.type),
            )
        except ObjectDoesNotExist:
            return None

    def list(self) -> List[CastMember]:
        cast_member_models = CastMemberModel.objects.all()
        return [
            CastMember(
                id=cast_member_model.id,
                name=cast_member_model.name,
                type=CastMemberType(cast_member_model.type),
            )
            for cast_member_model in cast_member_models
        ]

    def update(self, cast_member: CastMember) -> None:
        try:
            cast_member_model = CastMemberModel.objects.get(id=cast_member.id)
            cast_member_model.name = cast_member.name
            cast_member_model.type = cast_member.type.value
            cast_member_model.save()
        except ObjectDoesNotExist:
            raise ValueError(f"CastMember with id {cast_member.id} not found")

    def delete(self, id: UUID) -> None:
        try:
            cast_member_model = CastMemberModel.objects.get(id=id)
            cast_member_model.delete()
        except ObjectDoesNotExist:
            raise ValueError(f"CastMember with id {id} not found") 
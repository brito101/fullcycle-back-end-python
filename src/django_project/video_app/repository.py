from typing import List
from uuid import UUID

from django.db import transaction

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from .models import Video as VideoModel


class DjangoORMVideoRepository(VideoRepository):
    def save(self, video: Video) -> None:
        with transaction.atomic():
            video_model, _ = VideoModel.objects.update_or_create(
                id=video.id,
                defaults={
                    "title": video.title,
                    "description": video.description,
                    "launch_year": video.launch_year,
                    "duration": video.duration,
                    "rating": video.rating.value,
                    "opened": video.opened,
                    "published": video.published,
                }
            )

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoModel.objects.get(id=id)
            return self._to_domain(video_model)
        except VideoModel.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        VideoModel.objects.filter(id=id).delete()

    def update(self, video: Video) -> None:
        self.save(video)

    def list(self) -> List[Video]:
        video_models = VideoModel.objects.all()
        return [self._to_domain(video_model) for video_model in video_models]

    def _to_domain(self, video_model: VideoModel) -> Video:
        from src.core.video.domain.value_objects import Rating
        
        return Video(
            id=video_model.id,
            title=video_model.title,
            description=video_model.description,
            launch_year=video_model.launch_year,
            duration=video_model.duration,
            rating=Rating(video_model.rating),
            opened=video_model.opened,
            published=video_model.published,
            categories=set(),  # TODO: Implementar relacionamentos
            genres=set(),       # TODO: Implementar relacionamentos
            cast_members=set(), # TODO: Implementar relacionamentos
        )

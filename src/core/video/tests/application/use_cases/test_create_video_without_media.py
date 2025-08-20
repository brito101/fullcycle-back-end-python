from decimal import Decimal
from unittest.mock import create_autospec
from uuid import UUID, uuid4

import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.core.video.application.use_cases.exceptions import (
    InvalidVideo,
    RelatedEntitiesNotFound,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository


class TestCreateVideoWithoutMedia:
    @pytest.fixture
    def category_id(self) -> UUID:
        return uuid4()

    @pytest.fixture
    def genre_id(self) -> UUID:
        return uuid4()

    @pytest.fixture
    def cast_member_id(self) -> UUID:
        return uuid4()

    @pytest.fixture
    def mock_video_repository(self) -> VideoRepository:
        return create_autospec(VideoRepository)

    @pytest.fixture
    def mock_category_repository(self, category_id: UUID) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [create_autospec("Category", id=category_id)]
        return repository

    @pytest.fixture
    def mock_genre_repository(self, genre_id: UUID) -> GenreRepository:
        repository = create_autospec(GenreRepository)
        repository.list.return_value = [create_autospec("Genre", id=genre_id)]
        return repository

    @pytest.fixture
    def mock_cast_member_repository(self, cast_member_id: UUID) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = [create_autospec("CastMember", id=cast_member_id)]
        return repository

    def test_create_video_without_media_success(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
        category_id: UUID,
        genre_id: UUID,
        cast_member_id: UUID,
    ) -> None:
        # Arrange
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        request = CreateVideoWithoutMedia.Input(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            opened=False,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={category_id},
            genres={genre_id},
            cast_members={cast_member_id},
        )

        # Act
        output = use_case.execute(request=request)

        # Assert
        assert output.id is not None
        mock_video_repository.save.assert_called_once()

    def test_create_video_without_media_invalid_categories(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
        genre_id: UUID,
        cast_member_id: UUID,
    ) -> None:
        # Arrange
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        request = CreateVideoWithoutMedia.Input(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            opened=False,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={uuid4()},  # Invalid category ID
            genres={genre_id},
            cast_members={cast_member_id},
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound, match="Invalid categories"):
            use_case.execute(request=request)

        mock_video_repository.save.assert_not_called()

    def test_create_video_without_media_invalid_genres(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
        category_id: UUID,
        cast_member_id: UUID,
    ) -> None:
        # Arrange
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        request = CreateVideoWithoutMedia.Input(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            opened=False,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={category_id},
            genres={uuid4()},  # Invalid genre ID
            cast_members={cast_member_id},
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound, match="Invalid genres"):
            use_case.execute(request=request)

        mock_video_repository.save.assert_not_called()

    def test_create_video_without_media_invalid_cast_members(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
        category_id: UUID,
        genre_id: UUID,
    ) -> None:
        # Arrange
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        request = CreateVideoWithoutMedia.Input(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            opened=False,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={category_id},
            genres={genre_id},
            cast_members={uuid4()},  # Invalid cast member ID
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound, match="Invalid cast members"):
            use_case.execute(request=request)

        mock_video_repository.save.assert_not_called()

    def test_create_video_without_media_invalid_video_data(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
        category_id: UUID,
        genre_id: UUID,
        cast_member_id: UUID,
    ) -> None:
        # Arrange
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        request = CreateVideoWithoutMedia.Input(
            title="",  # Invalid: empty title
            description="A test video",
            launch_year=2022,
            opened=False,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={category_id},
            genres={genre_id},
            cast_members={cast_member_id},
        )

        # Act & Assert
        with pytest.raises(InvalidVideo):
            use_case.execute(request=request)

        mock_video_repository.save.assert_not_called()

    def test_create_video_without_media_multiple_validation_errors(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
        mock_cast_member_repository: CastMemberRepository,
    ) -> None:
        # Arrange
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        request = CreateVideoWithoutMedia.Input(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            opened=False,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={uuid4()},  # Invalid category ID
            genres={uuid4()},      # Invalid genre ID
            cast_members={uuid4()}, # Invalid cast member ID
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(request=request)

        assert "Invalid categories" in str(exc_info.value)
        assert "Invalid genres" in str(exc_info.value)
        assert "Invalid cast members" in str(exc_info.value)

        mock_video_repository.save.assert_not_called()

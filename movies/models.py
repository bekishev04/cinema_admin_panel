import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Base class for models with created_at/updated_at timestamps."""

    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Base class for models with generated UUID(Primary key)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_(_("genre_name")), max_length=100, unique=True)
    description = models.TextField(_("description"), null=True, blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("name"), max_length=200)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")


class FilmWork(UUIDMixin, TimeStampedMixin):
    class _FilmType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")
        __empty__ = _("null")

    title = models.CharField(_("film_name"), max_length=200)
    description = models.TextField(
        _("description"),
        null=True,
    )
    creation_date = models.DateField(
        _("creation date"),
        null=True,
    )
    file_path = models.DateField(
        _("file_path"),
        null=True,
    )
    rating = models.FloatField(
        _("rating"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100.0)],
    )
    type = models.CharField(
        _("type"),
        max_length=15,
        choices=_FilmType.choices,
        default=_FilmType.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")
    person = models.ManyToManyField(Person, through="PersonFilmWork")

    # If DB should check a field value, add "models.CheckConstraint" in "Meta"
    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film work")
        verbose_name_plural = _("film works")


class GenreFilmWork(UUIDMixin):
    """Many To Many for "FilmWork" and "Genre"."""

    film_work = models.ForeignKey(
        "FilmWork",
        on_delete=models.CASCADE,
        verbose_name=_("film work"),
        db_index=False,
    )
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("genre"), db_index=False
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("film genre")
        verbose_name_plural = _("film genres")
        constraints = [
            models.UniqueConstraint(
                fields=("film_work", "genre"), name="unique_film_genre"
            )
        ]
        indexes = [
            models.Index(fields=["film_work"], name="genre_film_work_film_work_id"),
            models.Index(fields=["genre"], name="genre_film_work_genre_id"),
        ]


class PersonFilmWork(UUIDMixin):
    """Many To Many for "FilmWork" and "Person"."""

    class Role(models.TextChoices):
        ACTOR = "actor", _("actor")
        DIRECTOR = "director", _("director")
        WRITER = "writer", _("writer")
        __empty__ = _("null")

    film_work = models.ForeignKey(
        "FilmWork",
        on_delete=models.CASCADE,
        verbose_name=_("film work"),
        db_index=False,
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("person"), db_index=False
    )
    role = models.CharField(_("role"), max_length=15, choices=Role.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("film person")
        verbose_name_plural = _("film persons")
        indexes = [
            models.Index(fields=["film_work"], name="person_film_work_film_work_id"),
            models.Index(fields=["person"], name="person_film_work_person_id"),
        ]
        # Mark For Reviewer:
        # Не добавляю ограниченность дублирования на поля "film_work", "person"
        # По причине того, что в исходной таблице sqlite данное возможно
        # Человек может быть одновременно актером и писателем или режиссером в одном фильме
        # Вот пример в данных того, о чем говорю:
        # (film_work_id, person_id)=('f94cfce9-fa49-4d36-ab4f-ae0ac9b6037b', 'f5ac8efa-1bd6-42ac-9c82-898146bcebdc')

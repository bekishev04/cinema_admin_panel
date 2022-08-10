from django.contrib import admin

from movies import models


def _all_fields(model):
    return [field.name for field in getattr(model, "_meta").fields]


class GenreFilmWorkInline(admin.TabularInline):
    model = models.GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = models.PersonFilmWork


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = _all_fields(models.Genre)

    list_filter = (models.Genre.updated_at.field.name,)

    search_fields = (
        models.Genre.name.field.name,
        models.Genre.description.field.name,
        models.Genre.id.field.name,
    )

    inlines = (GenreFilmWorkInline,)


@admin.register(models.GenreFilmWork)
class GenreFilmWorkAdmin(admin.ModelAdmin):

    list_display = _all_fields(models.GenreFilmWork)

    search_fields = (
        models.GenreFilmWork.created_at.field.name,
        models.GenreFilmWork.id.field.name,
    )


@admin.register(models.FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):

    list_display = _all_fields(models.FilmWork)

    list_filter = (models.FilmWork.type.field.name,)

    search_fields = (
        models.FilmWork.title.field.name,
        models.FilmWork.description.field.name,
        models.FilmWork.id.field.name,
    )

    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = _all_fields(models.Person)

    search_fields = (
        models.Person.full_name.field.name,
        models.Person.id.field.name,
    )

    inlines = (PersonFilmWorkInline,)


@admin.register(models.PersonFilmWork)
class PersonFilmWorkAdmin(admin.ModelAdmin):

    list_display = _all_fields(models.PersonFilmWork)

    list_filter = (models.PersonFilmWork.role.field.name,)

    search_fields = (
        models.PersonFilmWork.role.field.name,
        models.PersonFilmWork.id.field.name,
    )

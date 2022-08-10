from django.contrib import admin

from movies import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = models.FilmWork._get_FIELD_display
    # Фильтрация в списке
    list_filter = ("type",)

from django.contrib import admin

from .models import Culture
from .models import Farm
from .models import Productor
from .models import Season


@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "farm",
        "cpf_cnpj",
        "city",
        "state",
        "total_area",
        "agricultural_area",
        "vegetation_area",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "cpf_cnpj", "farm__name", "city", "state")
    list_filter = ("state",)
    ordering = ("name",)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("year",)
    search_fields = ("year",)
    ordering = ("year",)


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "season",
    )
    search_fields = (
        "name",
        "season__year",
    )
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

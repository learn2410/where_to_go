from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fk_name = "place"
    list_display = ('img_preview')
    fields = ['img', 'img_preview', 'number']
    readonly_fields = ('img_preview',)

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" height="200" />', mark_safe(obj.img.url))
        return ""

    img_preview.short_description = 'Preview'
    img_preview.allow_tags = True

    class Meta:
        ordering = ['number']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    ordering = ['title']
    inlines = [ImageInline, ]

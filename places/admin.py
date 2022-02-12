from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fk_name = "placeid"
    list_display = ('img_preview')
    fields = ['img', 'img_preview', 'number']
    readonly_fields = ('img_preview',)

    def img_preview(self, obj):
        return obj.img_preview

    img_preview.short_description = 'Preview'
    img_preview.allow_tags = True

    class Meta:
        ordering = ['number']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['title']
    inlines = [ImageInline, ]


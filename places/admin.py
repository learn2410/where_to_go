from django.contrib import admin

from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fk_name = "placeid"
    # list_display = ('img_preview' )
    fields=['img','img_preview','number']
    readonly_fields = ('img_preview',)

    def img_preview(self, obj):
        return obj.img_preview

    img_preview.short_description = 'Preview'
    img_preview.allow_tags = True

    class Meta:
        ordering = ['number']
        verbose_name = 'фото'
        verbose_name_plural = 'фотографии'


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['title']
    inlines = [
        ImageInline,
    ]


class ImageAdmin(admin.ModelAdmin):
    list_display = ('place_num', 'img_preview')
    list_filter = ['placeid']
    readonly_fields = ('img_preview',)
    ordering = ('placeid', 'number')

    def img_preview(self, obj):
        return obj.img_preview

    img_preview.short_description = 'Preview'
    img_preview.allow_tags = True

    class Meta:
        ordering = ['placeid', 'number']
        verbose_name = 'фото'
        verbose_name_plural = 'фотографии'


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image, ImageAdmin)

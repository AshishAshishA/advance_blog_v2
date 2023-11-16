from django.contrib import admin
from . import models

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "body",)
    prepopulated_fields = {"slug": ("title",)}

# Register your models here.
# admin.site.register(models.User)
# admin.site.register(ArticleAdmin)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Post,ArticleAdmin)


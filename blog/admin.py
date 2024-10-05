from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "pub_date", "user"]
    search_fields = ["title"]
    exclude = ["slug"]


admin.site.register(Post, PostAdmin)

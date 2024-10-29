from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "pub_date", "user"]
    search_fields = ["title"]
    exclude = ["slug"]


admin.site.register(Post, PostAdmin)

admin.site.site_header = "DB's Blog Administration"
admin.site.site_title = "Site Admin"
admin.site.index_title = "Admin Home"

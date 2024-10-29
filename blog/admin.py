from django.contrib import admin
from .models import Post


class CustomAdminSite(admin.AdminSite):
    site_header = "DB's Blog Administration"
    site_title = "DB's Blog site admin"


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "pub_date", "user"]
    search_fields = ["title"]
    exclude = ["slug"]


custom_admin_site = CustomAdminSite()

custom_admin_site.register(Post, PostAdmin)

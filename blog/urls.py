from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogPageView.as_view(), name="home"),
    path("search", views.SearchView.as_view(), name="search"),
    path("<int:year>/<int:month>/<slug:slug>", views.PostDetailView.as_view(), name="post_detail_view"),
]

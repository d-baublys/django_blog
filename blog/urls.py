from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogHomeView.as_view(), name="home"),
    path("search", views.SearchResultView.as_view(), name="search_results"),
    path("<int:year>/<int:month>/<slug:slug>", views.PostDetailView.as_view(), name="post_detail"),
]

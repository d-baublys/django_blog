from django.urls import path
from .views import BlogPageView, PostDetailView, SearchView

urlpatterns = [
    path('', BlogPageView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='search'),
    path('post/<int:post_id>', PostDetailView.as_view(), name='post_detail_view'),
]

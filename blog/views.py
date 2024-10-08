from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, View
from .models import Post
from .forms import SearchForm

class BlogPageView(ListView):
    model = Post
    template_name = "blog_page.html"
    context_object_name = "paginated_posts"
    paginate_by = 5
    ordering = "-pub_date"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm()
        context["tree_posts"] = self.object_list

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_object(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        slug = self.kwargs.get("slug")

        return get_object_or_404(Post, pub_date__year=year, pub_date__month=month, slug=slug)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        previous_post = Post.objects.filter(pub_date__lt=post.pub_date).order_by("-pub_date").first()
        next_post = Post.objects.filter(pub_date__gt=post.pub_date).order_by("pub_date").first()

        context["previous_post"] = previous_post
        context["next_post"] = next_post
        context["form"] = SearchForm()
        context["tree_posts"] = Post.objects.all().order_by("-pub_date")

        return context
    

class SearchView(ListView):
    model = Post
    template_name = "search_results.html"
    context_object_name = "results"
    paginate_by = 5

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("q")
            return (
                Post.objects.filter(title__icontains=query)
                | Post.objects.filter(content__icontains=query)
            ).order_by("-pub_date")
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm(self.request.GET)
        context["query"] = self.request.GET.get("q", "")
        context["tree_posts"] = Post.objects.all().order_by("-pub_date")

        return context

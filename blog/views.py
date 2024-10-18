from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils import timezone
from .forms import SearchForm
from .models import Post


class BlogHomeView(generic.ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "paginated_posts"
    paginate_by = 5
    ordering = "-pub_date"

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm()
        context["tree_posts"] = self.object_list

        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_object(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        slug = self.kwargs.get("slug")

        return get_object_or_404(Post, pub_date__year=year, pub_date__month=month, slug=slug, pub_date__lte=timezone.now())
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        previous_post = Post.objects.filter(pub_date__lt=post.pub_date).order_by("-pub_date").first()
        next_post = Post.objects.filter(pub_date__gt=post.pub_date, pub_date__lte=timezone.now()).order_by("pub_date").first()

        context["previous_post"] = previous_post
        context["next_post"] = next_post
        context["form"] = SearchForm()
        context["tree_posts"] = Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")

        return context
    

class SearchResultView(generic.ListView):
    model = Post
    template_name = "blog/results.html"
    context_object_name = "results"
    paginate_by = 5
    ordering = "-pub_date"

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("q")
            return (
                Post.objects.filter(title__icontains=query, pub_date__lte=timezone.now())
                | Post.objects.filter(content__icontains=query, pub_date__lte=timezone.now())
            ).order_by(self.ordering)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm(self.request.GET)
        context["query"] = self.request.GET.get("q", "")
        context["tree_posts"] = Post.objects.filter(pub_date__lte=timezone.now()).order_by(self.ordering)

        return context

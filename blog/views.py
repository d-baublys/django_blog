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
    ordering = ["-pub_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm()
        context["tree_posts"] = self.object_list

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

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
    

class SearchView(View):
    def get(self, request):
        form = SearchForm(request.GET)
        tree_posts = Post.objects.all().order_by("-pub_date")
        if form.is_valid():
            query = form.cleaned_data.get("query")
            results = (Post.objects.filter(title__icontains=query) 
                       | Post.objects.filter(content__icontains=query)).order_by("-pub_date")
            paginator = Paginator(results, 5)
            page = request.GET.get("page")

            try:
                page_results = paginator.page(page)
            except PageNotAnInteger:
                page_results = paginator.page(1)
            except EmptyPage:
                page_results = paginator.page(paginator.num_pages)
            
            return render(request, "search_results.html",
                        {"tree_posts": tree_posts, "form": form, "query": query, "results": page_results})
        
        return render(request, "search_results.html", {"tree_posts": tree_posts, "form": form})

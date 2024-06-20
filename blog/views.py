from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from .models import Post
from .forms import SearchForm

class BlogPageView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-pub_date')
        form = SearchForm()
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        try:
            page_posts = paginator.page(page)
        except PageNotAnInteger:
            page_posts = paginator.page(1)
        except EmptyPage:
            page_posts = paginator.page(paginator.num_pages)
        return render(request, 'blog_page.html', {'posts': posts, 'form': form, 'page_posts': page_posts})

class PostDetailView(View):
    def get(self, request, post_id):
        posts = Post.objects.all().order_by('-pub_date')
        post = get_object_or_404(Post, pk=post_id)
        form = SearchForm()
        return render(request, 'post_detail.html', {'posts': posts, 'post': post, 'form': form})

class SearchView(View):
    def get(self, request):
        if request.method == "GET":
            form = SearchForm(request.GET)
            posts = Post.objects.all().order_by('-pub_date')
            if form.is_valid():
                query = form.cleaned_data.get("query")
                results = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
                paginator = Paginator(results, 5)
                page = request.GET.get('page')
                try:
                    page_results = paginator.page(page)
                except PageNotAnInteger:
                    page_results = paginator.page(1)
                except EmptyPage:
                    page_results = paginator.page(paginator.num_pages)
                return render(request, 'search_results.html',
                            {'posts': posts, 'query': query, 'form': form, 'results': page_results})
            else:
                form = SearchForm()
            return render(request, 'search_results.html', {'posts': posts, 'form': form})

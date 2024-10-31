import datetime
import re

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from ..forms import SearchForm
from ..models import Post
from ..views import BlogHomeView, SearchResultView


# Helper functions
def create_post(
    user, title="Test Post", content="This is test content.", pub_date=None
):
    if pub_date is None:
        pub_date = timezone.now()

    return Post.objects.create(
        title=title, content=content, pub_date=pub_date, user=user
    )


def create_multiple_posts(user, post_count):
    for post_num in range(post_count):
        create_post(user=user, title=f"Test Post {post_num + 1}")


def create_date_staggered_posts(user):
    recent_post = create_post(
        user=user, title="Recent Title", content="This is recent content."
    )
    old_post = create_post(
        user=user,
        title="Old Title",
        content="This is old content.",
        pub_date=timezone.now() - datetime.timedelta(days=1),
    )
    oldest_post = create_post(
        user=user,
        title="Oldest Title",
        content="This is the oldest content.",
        pub_date=timezone.now() - datetime.timedelta(days=2),
    )

    return recent_post, old_post, oldest_post


def create_future_and_recent_post(user):
    future_post = create_post(
        user=user,
        title="Future Post",
        content="This is a future post.",
        pub_date=timezone.now() + datetime.timedelta(days=1),
    )
    recent_post = create_post(
        user=user,
        title="Recent Post",
        content="This is a recent post.",
        pub_date=timezone.now() - datetime.timedelta(days=1),
    )

    return future_post, recent_post


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test_user", password="12345")
        cls.paginate_by = BlogHomeView.paginate_by
        cls.multi_post_count = (cls.paginate_by * 3) // 2  # For pagination tests

    def test_view_at_exact_url(self):
        """
        Verify the view is accessible using the exact URL path.
        """
        response = self.client.get("")

        self.assertEqual(response.status_code, 200)

    def test_view_at_url_name(self):
        """
        Verify the view is accessible using the URLconf name.
        """
        response = self.client.get(reverse("blog:home"))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Verify the view renders the correct template.
        """
        response = self.client.get(reverse("blog:home"))

        self.assertTemplateUsed(response, "blog/home.html")

    def test_empty_post_listing(self):
        """
        Verify empty state message is shown in place of an empty post listing.
        """
        response = self.client.get(reverse("blog:home"))

        self.assertQuerySetEqual(response.context["paginated_posts"], [])
        self.assertContains(response, '<p class="empty-listing">No posts available.</p>')

    def test_post_listing(self):
        """
        Verify a post with a recent publication date is passed to the template
        and visible in the post listing.
        """
        post = create_post(user=self.user)
        response = self.client.get(reverse("blog:home"))

        # Avoid title search in the post tree
        title_search = re.search(
            rf'"title-link">\s*{post.title.upper()}', response.content.decode()
        )
        self.assertQuerySetEqual(response.context["paginated_posts"], [post])
        self.assertTrue(title_search)  # Check there is a match
        self.assertContains(response, post.content)

    def test_post_listing_order(self):
        """
        Verify the post listing is in descending order in the back-end and front-end.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(reverse("blog:home"))
        response_content = response.content.decode()

        self.assertQuerySetEqual(
            response.context["paginated_posts"], [recent_post, old_post, oldest_post]
        )

        # Compare indexes to check posts are rendered in the correct order
        self.assertTrue(
            response_content.index(f"{recent_post.content}")
            < response_content.index(f"{old_post.content}")
            < response_content.index(f"{oldest_post.content}")
        )

    def test_listing_excludes_future_posts(self):
        """
        Verify posts with a future publication date are not passed to the
        template and not visible in the post listing.
        """
        future_post, recent_post = create_future_and_recent_post(self.user)
        response = self.client.get(reverse("blog:home"))

        self.assertQuerySetEqual(response.context["paginated_posts"], [recent_post])

        # Avoid title search in the post tree
        recent_title_search = re.search(
            rf'"title-link">\s*{recent_post.title.upper()}', response.content.decode()
        )
        self.assertTrue(recent_title_search)
        self.assertContains(response, recent_post.content)

        # Avoid title search in the post tree
        future_title_search = re.search(
            rf'"title-link">\s*{future_post.title.upper()}', response.content.decode()
        )
        self.assertFalse(future_title_search)
        self.assertNotContains(response, future_post.content)

    def test_pagination_page_one(self):
        """
        Verify the first page contains paginate_by number of posts.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(reverse("blog:home"))

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["paginated_posts"]), self.paginate_by)

    def test_pagination_page_two(self):
        """
        Verify the second page contains the remaining posts.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(reverse("blog:home") + "?page=2")

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["paginated_posts"]),
            self.multi_post_count - self.paginate_by,
        )

    def test_invalid_page_url(self):
        """
        Verify that pages beyond num_pages of the paginator are not accessible.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(reverse("blog:home") + "?page=3")

        self.assertTrue(response.status_code, 404)

    def test_empty_post_tree(self):
        """
        Verify empty state message is shown in place of an empty post tree.
        """
        response = self.client.get(reverse("blog:home"))

        self.assertQuerySetEqual(response.context["tree_posts"], [])
        self.assertContains(response, "<p>No posts available.</p>")

    def test_tree_post_list(self):
        """
        Verify the post tree object list remains unpaginated.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(reverse("blog:home"))

        self.assertIn("tree_posts", response.context)
        self.assertTrue(len(response.context["tree_posts"]), self.multi_post_count)

    def test_tree_post_list_order(self):
        """
        Verify the post tree object list is in descending order in the back-end
        and front-end.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(reverse("blog:home"))
        response_content = response.content.decode()

        self.assertQuerySetEqual(
            response.context["tree_posts"], [recent_post, old_post, oldest_post]
        )

        # Compare indexes to check posts are rendered in the correct order
        self.assertTrue(
            response_content.index(f"{recent_post.title}")
            < response_content.index(f"{old_post.title}")
            < response_content.index(f"{oldest_post.title}")
        )

    def test_post_tree_excludes_future_posts(self):
        """
        Verify posts with a future publication date are not passed to the
        template and not visible in the post tree.
        """
        future_post, recent_post = create_future_and_recent_post(self.user)
        response = self.client.get(reverse("blog:home"))

        self.assertQuerySetEqual(response.context["tree_posts"], [recent_post])

        # Avoid title searches in the post listing
        recent_search = re.search(
            rf'"post-clamp">\s*{recent_post.title}', response.content.decode()
        )
        self.assertTrue(recent_search)

        future_search = re.search(
            rf'"post-clamp">\s*{future_post.title}', response.content.decode()
        )
        self.assertFalse(future_search)

    def test_search_form_integration(self):
        """
        Verify the search form is passed to the template and rendered.
        """
        response = self.client.get(reverse("blog:home"))

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], SearchForm)

        # Search for field name in the HTML to check form is rendered
        self.assertContains(response, 'name="q"')


class PostDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test_user", password="12345")
        cls.multi_post_count = 7

    def test_view_at_exact_url(self):
        """
        Verify the view is accessible using the exact URL path.
        """
        post = create_post(user=self.user)
        response = self.client.get(
            f"/{post.pub_date.year}/{post.pub_date.month}/{post.slug}"
        )

        self.assertEqual(response.status_code, 200)

    def test_view_at_url_name(self):
        """
        Verify the view is accessible using the URLconf name.
        """
        post = create_post(user=self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[post.pub_date.year, post.pub_date.month, post.slug],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_url(self):
        """
        Verify posts are not accessible with an invalid URL.
        """
        post = create_post(user=self.user)

        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[9999, post.pub_date.month, post.slug],
            )
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[post.pub_date.year, 99, post.slug],
            )
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[post.pub_date.year, post.pub_date.month, 12345],
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        """
        Verify the view renders the correct template.
        """
        post = create_post(user=self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[post.pub_date.year, post.pub_date.month, post.slug],
            )
        )

        self.assertTemplateUsed(response, "blog/detail.html")

    def test_future_post_not_accessible(self):
        """
        Verify posts with a future publication date are not accessible in the
        front-end.
        """
        post = create_post(
            user=self.user, pub_date=timezone.now() + datetime.timedelta(days=1)
        )
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[post.pub_date.year, post.pub_date.month, post.slug],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_previous_post(self):
        """
        Verify previous_post is the next oldest post.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[
                    recent_post.pub_date.year,
                    recent_post.pub_date.month,
                    recent_post.slug,
                ],
            )
        )

        self.assertEqual(response.context["previous_post"], old_post)

    def test_next_post(self):
        """
        Verify next_post is the next newest post.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[
                    oldest_post.pub_date.year,
                    oldest_post.pub_date.month,
                    oldest_post.slug,
                ],
            )
        )

        self.assertEqual(response.context["next_post"], old_post)

    def test_next_post_excludes_future_posts(self):
        """
        Verify posts with a future publication date are excluded from next_post.
        """
        future_post, recent_post = create_future_and_recent_post(self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[
                    recent_post.pub_date.year,
                    recent_post.pub_date.month,
                    recent_post.slug,
                ],
            )
        )

        self.assertIsNone(response.context["next_post"])

    def test_tree_post_list(self):
        """
        Verify the post tree object list is complete.
        """
        post = create_post(user=self.user)
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[post.pub_date.year, post.pub_date.month, post.slug],
            )
        )

        self.assertIn("tree_posts", response.context)
        self.assertTrue(len(response.context["tree_posts"]), self.multi_post_count + 1)

    def test_tree_post_list_order(self):
        """
        Verify the post tree object list is in descending order in the back-end
        and front-end.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[
                    recent_post.pub_date.year,
                    recent_post.pub_date.month,
                    recent_post.slug,
                ],
            )
        )
        response_content = response.content.decode()

        self.assertQuerySetEqual(
            response.context["tree_posts"], [recent_post, old_post, oldest_post]
        )

        # Compare indexes to check posts are rendered in the correct order
        self.assertTrue(
            response_content.index(f"{recent_post.title}")
            < response_content.index(f"{old_post.title}")
            < response_content.index(f"{oldest_post.title}")
        )

    def test_post_tree_excludes_future_posts(self):
        """
        Verify posts with a future publication date are not passed to the
        template and not visible in the post tree.
        """
        future_post, recent_post = create_future_and_recent_post(self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[
                    recent_post.pub_date.year,
                    recent_post.pub_date.month,
                    recent_post.slug,
                ],
            )
        )

        self.assertQuerySetEqual(response.context["tree_posts"], [recent_post])

        # Avoid title searches in the post listing
        recent_search = re.search(
            rf'"post-clamp">\s*{recent_post.title}', response.content.decode()
        )
        self.assertTrue(recent_search)

        future_search = re.search(
            rf'"post-clamp">\s*{future_post.title}', response.content.decode()
        )
        self.assertFalse(future_search)

    def test_search_form_integration(self):
        """
        Verify the search form is passed to the template and rendered.
        """
        post = create_post(user=self.user)
        response = self.client.get(
            reverse(
                "blog:post_detail",
                args=[post.pub_date.year, post.pub_date.month, post.slug],
            )
        )

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], SearchForm)

        # Search for field name in the HTML to check form is rendered
        self.assertContains(response, 'name="q"')


class SearchResultViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test_user", password="12345")
        cls.paginate_by = SearchResultView.paginate_by
        cls.multi_post_count = (cls.paginate_by * 3) // 2  # For pagination tests

    def test_view_at_exact_url(self):
        """
        Verify the view is accessible using the exact URL path.
        """
        response = self.client.get("/search")

        self.assertEqual(response.status_code, 200)

    def test_view_at_url_name(self):
        """
        Verify the view is accessible using the URLconf name.
        """
        response = self.client.get(reverse("blog:search_results"))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Verify the view renders the correct template.
        """
        response = self.client.get(reverse("blog:search_results"))

        self.assertTemplateUsed(response, "blog/results.html")

    def test_no_search_results(self):
        """
        Verify empty state message is shown when no results are found.
        """
        create_post(user=self.user)
        response = self.client.get(reverse("blog:search_results"), data={"q": "12345"})

        self.assertQuerySetEqual(response.context["results"], [])
        self.assertContains(response, '<p class="empty-results">No results found.</p>')

    def test_has_search_results(self):
        """
        Verify a post with a recent publication date is passed to the template
        and visible in the search results.
        """
        post = create_post(user=self.user)
        response = self.client.get(reverse("blog:search_results"), data={"q": "Test"})

        self.assertQuerySetEqual(response.context["results"], [post])

        # Avoid title searches in the post listing
        title_search = re.search(
            rf'"title-link">\s*{post.title.upper()}', response.content.decode()
        )
        self.assertTrue(title_search)
        self.assertContains(response, post.content)

    def test_search_case_insensitive(self):
        """
        Verify the post search is case-insensitive.
        """
        post = create_post(user=self.user)
        response = self.client.get(
            reverse("blog:search_results"), data={"q": "CONTENT"}
        )

        self.assertQuerySetEqual(response.context["results"], [post])

    def test_search_results_order(self):
        """
        Verify the search results are in descending order in the back-end and front-end.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(reverse("blog:search_results"), data={"q": "This"})
        response_content = response.content.decode()

        self.assertQuerySetEqual(
            response.context["results"], [recent_post, old_post, oldest_post]
        )

        # Compare indexes to check posts are rendered in the correct order
        self.assertTrue(
            response_content.index(f"{recent_post.content}")
            < response_content.index(f"{old_post.content}")
            < response_content.index(f"{oldest_post.content}")
        )

    def test_results_exclude_future_posts(self):
        """
        Verify posts with a future publication date are not passed to the
        template and not visible in the search results.
        """
        future_post, recent_post = create_future_and_recent_post(self.user)
        response = self.client.get(reverse("blog:search_results"), data={"q": "This"})

        self.assertQuerySetEqual(response.context["results"], [recent_post])

        # Avoid title search in the post tree
        recent_title_search = re.search(
            rf'"title-link">\s*{recent_post.title.upper()}', response.content.decode()
        )
        self.assertTrue(recent_title_search)
        self.assertContains(response, recent_post.content)

        # Avoid title search in the post tree
        future_title_search = re.search(
            rf'"title-link">\s*{future_post.title.upper()}', response.content.decode()
        )
        self.assertFalse(future_title_search)
        self.assertNotContains(response, future_post.content)

    def test_empty_query(self):
        """
        Verify an empty search query returns all posts.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(reverse("blog:search_results"), data={"q": ""})

        self.assertQuerySetEqual(
            response.context["results"], [recent_post, old_post, oldest_post]
        )

    def test_query_truncation(self):
        """
        Verify queries exceeding search form max length are truncated.
        """
        max_length = SearchForm().fields["q"].max_length
        query_length = max_length + 100
        long_query = "a" * query_length
        response = self.client.get(
            reverse("blog:search_results"), data={"q": long_query}
        )
        self.assertEqual(len(response.context["query"]), max_length)

    def test_pagination_page_one(self):
        """
        Verify the first page contains paginate_by number of search results.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(reverse("blog:search_results"), data={"q": "Test"})

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["results"]), self.paginate_by)

    def test_pagination_page_two(self):
        """
        Verify the second page contains the remaining results.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(
            reverse("blog:search_results"), data={"q": "Test", "page": 2}
        )

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["results"]),
            self.multi_post_count - self.paginate_by,
        )

    def test_invalid_page_url(self):
        """
        Verify that pages beyond num_pages of the paginator are not accessible.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(
            reverse("blog:search_results"), data={"q": "Test", "page": 3}
        )

        self.assertTrue(response.status_code, 404)

    def test_empty_post_tree(self):
        """
        Verify empty state message is shown in place of an empty post tree.
        """
        response = self.client.get(reverse("blog:search_results"))

        self.assertQuerySetEqual(response.context["tree_posts"], [])
        self.assertContains(response, "<p>No posts available.</p>")

    def test_tree_post_list(self):
        """
        Verify the post tree object list remains unpaginated.
        """
        create_multiple_posts(user=self.user, post_count=self.multi_post_count)
        response = self.client.get(reverse("blog:search_results"))

        self.assertIn("tree_posts", response.context)
        self.assertTrue(len(response.context["tree_posts"]), self.multi_post_count)

    def test_tree_post_list_order(self):
        """
        Verify the post tree object list is in descending order in the back-end
        and front-end.
        """
        recent_post, old_post, oldest_post = create_date_staggered_posts(user=self.user)
        response = self.client.get(reverse("blog:search_results"))
        response_content = response.content.decode()

        self.assertQuerySetEqual(
            response.context["tree_posts"], [recent_post, old_post, oldest_post]
        )

        # Compare indexes to check posts are rendered in the correct order
        self.assertTrue(
            response_content.index(f"{recent_post.title}")
            < response_content.index(f"{old_post.title}")
            < response_content.index(f"{oldest_post.title}")
        )

    def test_post_tree_excludes_future_posts(self):
        """
        Verify posts with a future publication date are not passed to the
        template and not visible in the post tree.
        """
        future_post, recent_post = create_future_and_recent_post(self.user)
        response = self.client.get(reverse("blog:search_results"))

        self.assertQuerySetEqual(response.context["tree_posts"], [recent_post])

        # Avoid title searches in the post listing
        recent_search = re.search(
            rf'"post-clamp">\s*{recent_post.title}', response.content.decode()
        )
        self.assertTrue(recent_search)

        future_search = re.search(
            rf'"post-clamp">\s*{future_post.title}', response.content.decode()
        )
        self.assertFalse(future_search)

    def test_search_form_integration(self):
        """
        Verify the search form is passed to the template and rendered.
        """
        response = self.client.get(reverse("blog:search_results"))

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], SearchForm)

        # Search for field name in the HTML to check form is rendered
        self.assertContains(response, 'name="q"')

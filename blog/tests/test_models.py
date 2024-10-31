from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from ..models import Post


# Helper function
def create_post(
    user, title="Test Post", content="This is test content.", pub_date=None
):
    if pub_date is None:
        pub_date = timezone.now()

    return Post.objects.create(
        title=title, content=content, pub_date=pub_date, user=user
    )


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test_user", password="12345")

    def test_title_length_limit(self):
        """
        Verify the title field adheres to the max_length limit.
        """
        post = create_post(user=self.user)
        max_len = post._meta.get_field("title").max_length
        self.assertEqual(max_len, 200)

    def test_pub_date_label(self):
        """
        Verify the custom verbose name is the expected label.
        """
        post = create_post(user=self.user)
        field_label = post._meta.get_field("pub_date").verbose_name
        self.assertEqual(field_label, "Date published")

    def test_slug_creation(self):
        """
        Verify the slug is created automatically from the title for new posts.
        """
        post = create_post(user=self.user, title="A TITLE to slugify: 123")
        self.assertEqual(post.slug, "a-title-to-slugify-123")

    def test_existing_slugs_unchanged(self):
        """
        Verify re-saving an existing post without modifying its title does not
        change its slug.
        """
        post = create_post(user=self.user, title="A TITLE to slugify: 123")
        slug_before = post.slug
        post.save()
        slug_after = post.slug
        self.assertEqual(slug_before, slug_after)

    def test_slug_changes_with_title(self):
        """
        Verify re-saving an existing post after modifying its title also updates
        its slug.
        """
        post = create_post(user=self.user, title="A TITLE to slugify: 123")
        slug_before = post.slug
        post.title = "This title has been changed"
        post.save()
        slug_after = post.slug
        self.assertNotEqual(slug_before, slug_after)

    def test_non_alpha_title_slug(self):
        """
        Verify posts with titles that cannot be slugified have a UUID as a slug
        and the resulting URL is accessible.
        """
        post = create_post(user=self.user, title="😀😀😀")
        self.assertRegex(post.slug, r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}")
        response = self.client.get(
            f"/{post.pub_date.year}/{post.pub_date.month}/{post.slug}"
        )
        self.assertEqual(response.status_code, 200)

    def test_unique_slug_condition(self):
        """
        Verify that posts with the same title and pub_date month and year cannot
        have identical slugs.
        """
        date_one = timezone.datetime(
            2024, 8, 10, tzinfo=timezone.get_current_timezone()
        )
        date_two = timezone.datetime(
            2024, 9, 10, tzinfo=timezone.get_current_timezone()
        )
        date_three = timezone.datetime(
            2025, 8, 10, tzinfo=timezone.get_current_timezone()
        )

        post_one = create_post(user=self.user, pub_date=date_one)
        post_two = create_post(user=self.user, pub_date=date_one)
        post_three = create_post(user=self.user, pub_date=date_two)
        post_four = create_post(user=self.user, pub_date=date_three)

        self.assertNotEqual(post_one.slug, post_two.slug)  # Same title/year/month
        self.assertEqual(post_one.slug, post_three.slug)  # Different month
        self.assertEqual(post_one.slug, post_four.slug)  # Different year

    def test_string_representation(self):
        post = create_post(user=self.user)
        self.assertEqual(post.title, str(post))

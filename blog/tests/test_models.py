from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from ..models import Post


def create_post(title="Test Post", content="", pub_date=None, user=None):
    if pub_date is None:
        pub_date = timezone.now()
    return Post.objects.create(title=title, content=content, pub_date=pub_date, user=user)


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="12345")

    def test_title_length_limit(self):
        post = create_post(user=self.user)
        max_len = post._meta.get_field("title").max_length
        self.assertEqual(max_len, 200)

    def test_pub_date_label(self):
        post = create_post(user=self.user)
        field_label = post._meta.get_field("pub_date").verbose_name
        self.assertEqual(field_label, "Date published")

    def test_slug_creation(self):
        post = create_post(title="A slugified TITLE: 123", user=self.user)
        self.assertEqual(post.slug, "a-slugified-title-123")

    def test_string_representation(self):
        post = create_post(user=self.user)
        self.assertEqual(post.title, str(post))
       
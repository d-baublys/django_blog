from django.test import TestCase
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        Post.objects.create(name="test")

    def test_post_creation(self):
        test_post = Post.objects.get(name="test")
        self.assertEqual(test_post.name, "test")

    def test_string_representation(self):
        test_post = Post(title="Test Post")
        self.assertEqual(str(test_post), test_post.title)


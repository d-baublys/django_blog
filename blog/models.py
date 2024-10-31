from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    pub_date = models.DateTimeField("Date published")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="", max_length=200)

    def get_slug(self, title):
        original_slug = slugify(title)
        unique_slug = original_slug
        counter = 1
        while Post.objects.filter(
            slug=unique_slug,
            pub_date__year=self.pub_date.year,
            pub_date__month=self.pub_date.month,
        ).exists():
            unique_slug = f"{original_slug}-{counter}"
            counter += 1

        return unique_slug

    def save(self, *args, **kwargs):
        if not self.pk or (
            self.pk and Post.objects.get(pk=self.pk).title != self.title
        ):
            self.slug = self.get_slug(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField("Date published")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    blog_title = models.CharField(max_length=50)
    blog_body = models.TextField()

    def __str__(self):
        return self.blog_title
    

class Comments(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment
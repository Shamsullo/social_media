from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models

User = get_user_model()


class PostLike(models.Model):
    """Many to many table for posts and likes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    """User's post"""
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='post',
                               verbose_name=_('Post author'))
    content = models.TextField(verbose_name=_('Post content'), blank=True,
                               null=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True,
                                   through='PostLike')
    image = models.FileField(verbose_name=_('Post Image'), upload_to='images/',
                             blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name=_('Created date'),
                                     auto_now_add=True, )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.content[:100]

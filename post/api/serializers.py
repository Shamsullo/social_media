from datetime import datetime
from django.db.models import Count
from rest_framework import serializers

from ..models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'likes', 'timestamp']

    def get_likes(self, post):
        return post.likes.count()

    # def get_author(self, obj):
    #     return self.context.get('request').user.id


class SinglePostAnalyticsSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'likes']

    def get_likes(self, post):
        params = self.context.get('request').GET
        date_from = datetime.strptime(params['date_from'],
                                      '%Y-%m-%d').astimezone()
        date_to = datetime.strptime(params['date_to'],
                                    '%Y-%m-%d').astimezone()

        likes_by_day = PostLike.objects\
            .filter(post=post, timestamp__gte=date_from, timestamp__lte=date_to)\
            .values('timestamp__day')\
            .annotate(likes=Count('timestamp__day'))\
            .values('timestamp__date', 'likes')

        return likes_by_day

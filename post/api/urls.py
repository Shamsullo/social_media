from django.urls import path

from .views import (
    PostCreateView, LikeView, SinglePostAnalyticsView, PostsAnalyticsView
)

urlpatterns = [
    path('post/', PostCreateView.as_view(), name='create_post'),
    path('like/<int:pk>', LikeView.as_view(), name='like_post'),
    path('analytics/<int:pk>', SinglePostAnalyticsView.as_view(),
         name='single_post_analytics'),
    path('analytics/', PostsAnalyticsView.as_view(), name='post_analytics'),
]

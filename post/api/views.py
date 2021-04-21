from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import PostSerializer, SinglePostAnalyticsSerializer
from ..models import Post, PostLike


class PostCreateView(generics.CreateAPIView):
    """Post Creation"""
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class LikeView(APIView):
    """
    Handling like and unlike. By sending request to this endpoint, post will be
    liked by the user of unliked if he/she has already has liked the post.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, pk, ):
        post = self.get_object(pk)
        if PostLike.objects.filter(post=post).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=200)


class SinglePostAnalyticsView(generics.RetrieveAPIView):
    """All the analytics of the post details will implemented here"""
    permission_classes = (IsAuthenticated,)
    serializer_class = SinglePostAnalyticsSerializer
    queryset = Post.objects.all()


class PostsAnalyticsView(generics.ListAPIView):
    permission_classes = ()
    serializer_class = SinglePostAnalyticsSerializer
    queryset = Post.objects.all()


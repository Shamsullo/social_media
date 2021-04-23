import datetime
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from post.models import Post

User = get_user_model()


class PostTests(APITestCase):
    """Post creation and other post actions testing."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testUser', password='somepassword')
        self.authenticate_user()

        Post.objects.create(author=self.user, content='first post from setUp')

    def authenticate_user(self):
        login_url = reverse('jwt-create')
        response = self.client.post(login_url, {'username': 'testUser', 'password': 'somepassword'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['access'])

    def test_post_creation(self):
        """
        Ensure we can create a post using our endpoint.
        """
        url = reverse('create_post')
        data = {'content': 'some post content'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], data['content'])
        self.assertEqual(Post.objects.count(), 2)
        post = Post.objects.get(id=2)
        self.assertEqual(post.author, self.user)

        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_and_unlike_action(self):
        url = reverse('like_post', kwargs={'pk': 1})

        response = self.client.put(url)
        like_count = response.json().get("likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        user = self.user
        my_like_instances_count = user.postlike_set.count()
        self.assertEqual(my_like_instances_count, 1)

        response = self.client.put(url)
        like_count = response.json().get("likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 0)
        user = self.user
        my_like_instances_count = user.postlike_set.count()
        self.assertEqual(my_like_instances_count, 0)

    def test_single_like_analytics(self):

        url = reverse('single_post_analytics', kwargs={'pk': 1})
        today = datetime.date.today()
        date_from = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        date_to = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        params = {
            "date_from": date_from,
            "date_to": date_to
        }
        url_param = urlencode(params)
        url = f'{url}?{url_param}'
        response = self.client.get(url)
        self.assertEqual(response.data['likes'].count(), 0)

        like_url = reverse('like_post', kwargs={'pk': 1})

        response = self.client.put(like_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url)
        self.assertEqual(response.data['likes'].count(), 1)

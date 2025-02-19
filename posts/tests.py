from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.post = Post.objects.create(author=self.user, content='Test content')

    def test_post_creation(self):
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.content, 'Test content')

class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.post = Post.objects.create(author=self.user, content='Test content')
        self.client.force_authenticate(user=self.user)

    def test_get_post_detail(self):
        url = reverse('post-detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test content')

# Add more tests for other models and views as needed

from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from blog.models import Post
# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username="trump", password="somepassword")

    def test_landing(self):
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content="Hello World!! We are the world...",
            author=self.user_trump
        )
        post_002 = Post.objects.create(
            title='두번째 포스트 입니다.',
            content="1등이 전부가 아니잖아요",
            author=self.user_trump
        )
        post_003 = Post.objects.create(
            title='세번째 파이썬 포스트 입니다.',
            content="세번째 포스트 입니다.",
            author=self.user_trump
        )
        post_004 = Post.objects.create(
            title='파이썬에 대한 포스트입니다.',
            content="Hello World...",
            author=self.user_trump
        ) # 가장 최근에 만들어진 포스트가 004

        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn(post_001.title, body.text)
        self.assertIn(post_002.title, body.text)
        self.assertIn(post_003.title, body.text)
        self.assertIn(post_004.title, body.text)
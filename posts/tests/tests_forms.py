import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import path, reverse

from posts import views
from posts.forms import PostForm
from posts.models import Follow, Group, Post, User


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем временную папку для медиа-файлов;
        # на момент теста медиа папка будет перопределена
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        group = Group.objects.create(
            title='Заголовок',
            slug='test-slug',
            description='Описание',
        )
        user = User.objects.create(
            first_name='Name',
            last_name='Lastname',
            username='username',
            email='email'
        )



        Post.objects.create(
            text='Тестовый текст',
            group= group,
            author=user,
        )



        cls.form = PostForm()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = User.objects.get(username='username')
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

    def test_create_post(self):
        post_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый текст1',
            'image':uploaded,
        }

        response = self.authorized_client.post("/new/", data=form_data)
        self.assertRedirects(response, '/')
        self.assertEqual(Post.objects.count(), post_count + 1)

    def test_edit_post(self):
        post = get_object_or_404(Post, text= 'Тестовый текст')
        post.text = 'text'
        response = self.authorized_author.post('/username/1/edit')
        self.assertEqual(post.text,'text')



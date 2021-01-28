import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Follow, Group, Post, User


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
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
            id = 1,
            text='Текст',
            author=user,
            group=group,
            image=uploaded
        )

        user2 = User.objects.create(
            first_name='Name1',
            last_name='Lastname1',
            username='username1',
            email='email1'
        )
        # follow = Follow(
        #     user=user,
        #     author=user2
        # )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Рекурсивно удаляем временную после завершения тестов
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаём неавторизованный клиент
        self.guest_client = Client()
        # Создаём авторизованный клиент
        self.user = get_user_model().objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = User.objects.get(username='username')
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

    def test_pages_uses_correct_template(self):
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_page_names = {
            'index.html': reverse('posts'),
            'new_post.html': reverse('new_post'),
            'group.html': (
                reverse('group_posts', kwargs={'slug': 'test-slug'})
            ),
        }

        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_posts_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts'))
        post_text_0 = response.context.get('page')[0].text
        post_image = response.context.get('page')[0].image
        self.assertEqual(post_text_0, 'Текст')
        self.assertEqual(post_image.name,'posts/small.gif')

    def test_group_pages_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'})
            )
        post_image = response.context.get('posts')[0].image
        self.assertEqual(post_image.name, 'posts/small.gif')
        self.assertEqual(response.context.get('group').title, 'Заголовок')
        self.assertEqual(response.context.get('group').description, 'Описание')
        self.assertEqual(response.context.get('group').slug, 'test-slug')

    def test_posts_group_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts'))
        response1 = self.authorized_client.get(reverse('group_posts', kwargs={'slug': 'test-slug'}))
        post_group = response.context.get('page')[0].group
        post_group_groups = response1.context.get('group').title
        self.assertEqual(post_group.title, 'Заголовок')
        self.assertEqual(post_group_groups,'Заголовок')

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_author.get('/username/1/edit')
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
            # 'image': forms.fields.ImageField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_profile_pages_show_correct_context(self):
        response = self.authorized_client.get('/username/')
        post_image = response.context.get('posts')[0].image
        self.assertEqual(post_image.name, 'posts/small.gif')
        self.assertEqual(response.context.get('profile').username, 'username')
        self.assertEqual(response.context.get('profile').first_name,'Name')
        self.assertEqual(response.context.get('profile').last_name,'Lastname')

    def test_profile_post_page_show_correct_context(self):
        response = self.authorized_client.get('/username/1/')
        self.assertEqual(response.context.get('post').image, 'posts/small.gif')
        self.assertEqual(response.context.get('post').text, 'Текст')

    def test_follow_test(self):
        count = Follow.objects.count()
        response = self.authorized_client.get('/username/follow/')
        count_now = Follow.objects.count()
        self.assertEqual(count_now, count + 1)

    def test_page_favourite_authors(self):
        self.authorized_client.get('/username/follow/')
        response = self.authorized_client.get('/follow/')
        post_text_0 = response.context.get('page')[0].text
        self.assertEqual(post_text_0, 'Текст')

    # def test_post_edit_page_show_correct_context(self):
    #     response = self.authorized_author.get('/username/1/edit/')
    #     self.assertEqual(response.context.get('form').text, 'Текст')



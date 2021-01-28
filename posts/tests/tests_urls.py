from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
         super().setUpClass()

         # Создадим запись в БД для проверки доступности адреса task/test-slug/
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

         post = Post.objects.create(
             id = 1,
             text='Текст',
             author= user,
             group=group
         )

    def setUp(self):
         self.guest_client = Client()
         # Создаём авторизованный клиент
         self.user = get_user_model().objects.create_user(username='StasBasov')
         self.authorized_client = Client()
         self.authorized_client.force_login(self.user)
         self.author = User.objects.get(username='username')
         self.authorized_author = Client()
         self.authorized_author.force_login(self.author)

    def test_home_url_exists_at_desired_location(self):
         response = self.guest_client.get('/')
         self.assertEqual(response.status_code, 200)

    def test_group_url_exists_at_desired_location(self):
          response = self.guest_client.get('/group/test-slug/')
          self.assertEqual(response.status_code, 200)

    def test_post_added_url_exists_at_desired_location(self):
         response = self.authorized_client.get('/new/')
         self.assertEqual(response.status_code, 200)

    def test_profile_url_exists_at_desired_location(self):
          response = self.guest_client.get('/username/')
          self.assertEqual(response.status_code, 200)

    def test_post_url_exists_at_desired_location(self):
          response = self.guest_client.get('/username/1/')
          self.assertEqual(response.status_code, 200)

    def test_post_edit_url_exists_for_anonymous_user(self):
         response = self.guest_client.get('/username/1/edit/')
         self.assertNotEqual(response.status_code, 200)

    def test_post_edit_url_exists_for_author_user(self):
         response = self.authorized_author.get('/username/1/edit')
         self.assertEqual(response.status_code, 200)

    def test_post_edit_url_exists_for_not_author_user(self):
         response = self.authorized_client.get('/username/1/edit/')
         self.assertNotEqual(response.status_code, 200)



    def test_post_list_url_redirect_anonymous_on_admin_login(self):
         response = self.guest_client.get('/new/', follow=True)
         self.assertRedirects(
             response, '/auth/login/?next=/new/')

    def test_urls_uses_correct_template(self):
         templates_url_names = {
             'index.html': '/',
             'group.html': '/group/test-slug/',
             'new_post.html': '/new/',
             'post_new.html' : '/username/1/edit',

         }
         for template, url in templates_url_names.items():
             with self.subTest(url=url):
                 response = self.authorized_author.get(url)
                 self.assertTemplateUsed(response, template)

    def test_post_edit_user_without_permission(self):
        response = self.guest_client.get('/username/1/edit', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/username/1/edit')

    def test_comment_page_authorized_client(self):
        response = self.authorized_client.get('/username/1/comment')
        self.assertEqual(response.status_code,200)

    def test_comment_page_non_authorized_client(self):
        response = self.client.get('/username/1/comment')
        self.assertNotEqual(response.status_code, 200)
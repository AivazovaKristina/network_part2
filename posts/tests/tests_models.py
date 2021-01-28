from django.test import TestCase

from posts.models import Group, Post, User


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        Group.objects.create(
            id = 1,
            title= 'Заголовок',
            description = 'Описание',
        )

        cls.group = Group.objects.get(id=1)

    def test_verbose_name(self):
        group = GroupModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес для страницы группы',
            'description' : 'Описание'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_help_texts = {
            'title': 'Дайте название Вашему посту',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)


    def test_object_name_is_title_field(self):
        """В поле __str__  объекта task записано значение поля task.title."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))



class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(
            id = 1,
            first_name = 'Name',
            last_name = 'Lastname',
            username = 'username',
            email = 'email'
        )
        group = Group.objects.create(
            id = 2,
            title= 'Заголовок',
            description = 'Описание',)

        Post.objects.create(
            id = 1,
            text= 'Текст',
            author= user,
            group= group
        )

        cls.post = Post.objects.get(id=1)

    def test_verbose_name(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст',
            'pub_date': 'date published',

        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Напишите свой пост',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)


    def test_object_name_is_text_field(self):
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))
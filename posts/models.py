from django.contrib.auth import get_user_model
from django.db import models
# from users.models import Comment
from django.utils.text import slugify

from users.forms import User

# Create your models here.


class Group(models.Model):
    title = models.CharField(verbose_name='Заголовок',max_length=200,help_text='Дайте название Вашему посту')
    slug = models.SlugField(verbose_name='Адрес для страницы группы',unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст',help_text='Напишите свой пост')
    pub_date = models.DateTimeField('date published',auto_now_add=True, db_index=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,blank=True,null=True,on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.id


class Follow(models.Model):
    user = models.ForeignKey(User,related_name='follower', on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return self.user

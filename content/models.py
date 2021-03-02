from django.db import models

from users.models import User
from .validators import validate_year

class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)



class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)





class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(validators=[validate_year],db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category_titles', null=True)
    # rating = models.IntegerField()
    genre = models.ManyToManyField(Genre, related_name='genre_titles',
                                   blank=True)
    description = models.TextField(blank=True)
    # review = models.ManyToManyField(Review, related_name='reviews', blank=True )

    class Meta:
        ordering = ('year',)


class Review(models.Model):
    text = models.TextField(blank=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.CharField(max_length=10)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


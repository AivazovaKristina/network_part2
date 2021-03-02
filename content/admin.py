from django.contrib import admin
from .models import Genre,Comment,Category,Title,Review

# Register your models here.
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Review)


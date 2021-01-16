from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index, name='posts'),
    path('group/<slug:slug>',views.group_posts, name = 'group_posts'),
    path('new/', views.new_post,name='new_post'),
    ]

from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from posts import views

handler404 = 'posts.views.page_not_found'
handler500 = 'posts.views.server_error'


urlpatterns = [

    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('',views.index, name='posts'),
    path('<str:username>/<int:post_id>/comment', views.add_comment, name='add_comment'),
    path('group/<slug:slug>/',views.group_posts, name='group_posts'),
    path('follow/', views.follow_index, name='follow_index'),
    path('<str:username>/follow/', views.profile_follow, name = 'profile_follow'),
    path('<str:username>/unfollow/', views.profile_unfollow, name = 'profile_unfollow'),
    path('new/', views.new_post, name='new_post'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('about/', include('django.contrib.flatpages.urls')),
    path('user/login/', auth_views.LoginView.as_view(),name ='login'),
    path('logout/', auth_views.LogoutView.as_view()),
    path('new_user/password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('user/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls))),
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)


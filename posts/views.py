from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_page
from users.forms import User
from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post

# from users.models import Comment
# Create your views here.


# @cache_page(20)
def index(request):
    user = request.user
    post_list = Post.objects.select_related('group').order_by('-pub_date')
    paginator = Paginator(post_list,9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'user': user, 'paginator': paginator,})


def group_posts(request, slug):
    user = request.user
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    return render(request,'group.html', {'group': group, 'posts': posts, 'user':user})


@login_required
def new_post(request):
    error = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
        else:
            error='Форма была неверной'
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form,
                                             'error': error})


def profile(request, username):
    user = request.user
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile).order_by('-pub_date')
    if user.is_authenticated:
        following = Follow.objects.filter(author=profile, user=request.user)
        followers = Follow.objects.filter(author=profile)
        follow = Follow.objects.filter(user=profile)
        return render(request, 'profile.html',
                      {'posts': posts, 'profile': profile, 'user': user, 'following': following, 'followers': followers,
                       'follow': follow})

    return render(request, 'profile.html',
                  {'posts': posts, 'profile': profile, 'user': user})


def post_view(request, username, post_id):
    user = request.user
    profile = get_object_or_404(User, username =username)
    posts = Post.objects.filter(author=profile).order_by('-pub_date')
    post = get_object_or_404(posts, id=post_id)
    if user.is_authenticated:
        following = Follow.objects.filter(author=profile, user=request.user)
        followers = Follow.objects.filter(author=profile)
        follow = Follow.objects.filter(user=profile)
        comments = Comment.objects.filter(post=post).order_by('created')
        return render(request, 'post.html',
                      {'user': user, 'follow': follow, 'following': following, 'followers': followers,
                       'profile': profile, 'post': post, 'posts': posts, 'comments': comments})

    comments = Comment.objects.filter(post=post).order_by('created')
    return render(request, 'post.html',
                  {'user': user,'profile': profile, 'post': post, 'posts': posts, 'comments': comments})


@login_required
def add_comment(request, post_id,username):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('add_comment', username=username, post_id=post_id)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(post=post)
    return render(request, 'comments.html', {'form':form, 'comments':comments})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = get_object_or_404(User, username=username)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username=request.user.username, post_id=post_id)

    return render(request, 'post_new.html', {'form': form, 'post': post})


def page_not_found(request,exception):
    return render(
        request,
        'misc/404.html',
        {'path':request.path},
        status=404
    )


def server_error(request):
    return render(request,'misc/500.html',status=500)


@login_required
def follow_index(request):
    user = get_object_or_404(User, username=request.user.username)
    posts = Post.objects.filter(author__following__user = user).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    user = request.user
    if not Follow.objects.filter(author=author,user=user).exists():
        follower = Follow.objects.create(author=author, user=user)
        follower.save()
    return redirect('profile',username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    user = request.user
    obj = Follow.objects.filter(author=author,user=user)
    obj.delete()
    return redirect('profile',username)

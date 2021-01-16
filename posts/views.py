from django.shortcuts import render,get_object_or_404,redirect
from .models import Post, Group
from .forms import PostForm
# Create your views here.


def index(request):
    posts = Post.objects.order_by("-pub_date")[:10]
    return render(request,"index.html" , {'posts' : posts})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request,"group.html", {"group": group, "posts": posts})


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
            error="Форма была неверной"
    else:
        form = PostForm

    if request.user.is_authenticated:
        return render(request,'new_post.html',{'form':form,
             'error':error})
    else:
        return redirect('login')
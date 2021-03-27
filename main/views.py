from django.shortcuts import render, get_object_or_404
from .models import Post, Comment


def home(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "main/home.html", context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    context = {"post": post, "comments": comments}
    return render(request, "main/detail.html", context)
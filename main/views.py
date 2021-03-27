from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def home(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "main/home.html", context)


def detail(request, author, slug):
    try:
        author = User.objects.get(username=author)
    except:
        author = None
    post = get_object_or_404(Post, slug=slug, author=author)
    comments = post.comments.all()
    context = {"post": post, "comments": comments}
    return render(request, "main/detail.html", context)


def register(request):
    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Succesfully registered {username}. You can now log in.",
            )
            return redirect("main:login")
    else:
        form = UserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "main/register.html", context)


@login_required
def add_post(request):
    if request.method == "GET":
        return render(request, "main/addpost.html", {"form": PostForm})
    else:
        user = User.objects.get_by_natural_key(request.user.username)
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                author=user,
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                short_desc=form.cleaned_data["short_desc"],
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                "Post succesfully added",
            )
            return redirect("main:home")


@login_required
def edit(request):
    if request.method == "POST":
        user = User.objects.get_by_natural_key(request.user.username)
        id = request.POST.get("id")
        post = Post.objects.get(id=id)
        if post.author == user:
            return render(request, "main/editpost.html", {"post": post})


@login_required
def update(request):
    if request.method == "POST":
        user = User.objects.get_by_natural_key(request.user.username)
        id = request.POST.get("id")
        post = Post.objects.get(id=id)
        if post.author == user:
            post.title = request.POST.get("title")
            post.content = request.POST.get("content")
            post.short_desc = request.POST.get("short_desc")
            post.save()
    return redirect("main:dashboard")


@login_required
def dashboard(request):
    user = User.objects.get_by_natural_key(request.user.username)
    posts = Post.objects.filter(author=user)
    return render(request, "main/dashboard.html", {"posts": posts})


@login_required
def delete(request):
    if request.method == "POST":
        user = User.objects.get_by_natural_key(request.user.username)
        id = request.POST.get("id")
        post = Post.objects.get(id=id)
        if post.author == user:
            post.delete()

    return redirect("main:dashboard")


def add_comment(request):
    if request.method == "POST":
        id = request.POST.get("id")
        post = Post.objects.get(id=id)
        content = request.POST.get("content")
        Comment.objects.create(post=post, content=content)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

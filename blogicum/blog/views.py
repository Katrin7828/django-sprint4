from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.http import Http404

from .models import Post, Category
from .forms import CongratulationForm

POSTS_LIMIT = 5


def posts():
    """Получаем данные из таблиц."""
    date_now = timezone.now()
    return (
        Post.objects.select_related(
            'category',
            'location',
            'author',
        )
        .only(
            'title',
            'text',
            'pub_date',
            'author__username',
            'category__title',
            'category__slug',
            'location__name',
        )
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=date_now,
        ).order_by('-pub_date')
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'location', 'is_published',
                  'image']


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def index(request):
    """Выводит записи на главную страницу с пагинацией."""
    date_now = timezone.now()
    posts = Post.objects.filter(is_published=True,
                                pub_date__lte=date_now).order_by('-pub_date')
    post_list = posts()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    """Выводит отдельную страницу поста."""
    template = 'blog/detail.html'
    post = get_object_or_404(posts(), id=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Выводит страницу категории с пагинацией."""
    category = get_object_or_404(Category, slug=category_slug)
    post_list = posts().filter(category__slug=category_slug)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_owner = request.user.is_authenticated and request.user == user
    context = {'user_profile': user, 'page_obj': page_obj,
               'is_owner': is_owner}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', id=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/create_post.html', {'form': form,
                                                         'post': post})


@login_required
def add_congratulation(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CongratulationForm(request.POST)
        if form.is_valid():
            congratulation = form.save(commit=False)
            congratulation.post = post
            congratulation.author = request.user
            congratulation.save()
            return redirect('blog:post_detail', id=post.id)
        else:
            form = CongratulationForm()
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return Http404('У вас нет прав для удаления этого поста')
    if request.method == 'POST':
        post.delete()
        return redirect('blog:user_profile', username=request.user.username)
    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def toggle_publish(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not request.user.is_staff:
        return Http404('У вас нет прав для изменения статуса публикации')
    post.is_published = not post.is_published
    post.save()
    return redirect('blog:post_detail', id=post.id)


def test_email(request):
    pass
    return (request, 'blog:index')

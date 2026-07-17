from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import Count

from .models import Post, Category, Congratulation
from .forms import CommentForm, UserProfileForm

POSTS_LIMIT = 10


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
            if not post.pub_date:
                post.pub_date = timezone.now()
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


def index(request):
    post_list = posts().annotate(comment_count=Count('congratulations'))
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    """Выводит отдельную страницу поста."""
    template = 'blog/detail.html'
    try:
        post = Post.objects.get(id=id, is_published=True,
                                pub_date__lte=timezone.now())
    except Post.DoesNotExist:
        post = get_object_or_404(Post, id=id)
        if request.user != post.author:
            raise Http404("Пост не найден или недоступен")
    comments = Congratulation.objects.filter(
        post=post).order_by('created_at')
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = posts().filter(category__slug=category_slug).annotate(
        comment_count=Count('congratulations'))
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    is_owner = request.user.is_authenticated and request.user == user
    if is_owner:
        posts = Post.objects.filter(author=user).order_by('-pub_date')
    else:
        posts = Post.objects.filter(
            author=user,
            is_published=True,
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')
    posts = posts.annotate(comment_count=Count('congratulations'))
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': user,
        'page_obj': page_obj,
        'is_owner': is_owner,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', id=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            is_published = form.cleaned_data.get('is_published')
            if is_published is not None:
                post.is_published = is_published
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return render(request, 'pages/404.html', status=404)
    post.delete()
    return redirect('blog:profile', username=request.user.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Congratulation.objects.create(
                text=form.cleaned_data['text'],
                post=post,
                author=request.user,
            )
            return redirect('blog:post_detail', id=post.id)
        else:
            comments = Congratulation.objects.filter(
                post=post,
                is_approved=True).order_by('created_at')
            return render(request, 'blog/detail.html', {
                'post': post,
                'form': form,
                'comments': comments,
            })
    return redirect('blog:post_detail', id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(Congratulation, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html', {'form': form,
                                                 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Congratulation, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})


@login_required
def edit_profile(request):
    """Редактирование профиля текущего пользователя."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'blog/user.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from blog.models import Post
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.core.paginator import Paginator
from django.contrib.auth import logout

from .forms import CustomUserCreationForm, EditUserProfileForm


User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:index')
        else:
            form = UserCreationForm()
            return render(request, 'auth/registration.html', {'form': form})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    is_owner = request.user.is_authenticated and request.user == user

    context = {
        'user_profile': user,
        'posts': posts,
        'is_owner': is_owner,
    }
    return render(request, 'users/profile.html', context)


class UserCreateView(CreateView):
    template_name = "registration/registration_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("blog:index")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserProfileForm
    template_name = "blog/user.html"

    def get_object(self):
        return self.request.user


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_owner = request.user.is_authenticated and request.user == user
    context = {'user_profile': user, 'page_obj': page_obj,
               'is_owner': is_owner}
    return render(request, 'blog/profile.html', context)


def custom_logout(request):
    """Выход из системы с поддержкой GET-запросов."""
    logout(request)
    return redirect('blog:index')

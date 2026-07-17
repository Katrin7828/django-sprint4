from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

app_name = 'blog'

post_urls = [
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
]

profile_urls = [
    path('', views.user_profile, name='profile'),
]

category_urls = [
    path('<slug:category_slug>/', views.category_posts, name='category_posts'),
]

auth_urls = [
    path('registration/', views.UserCreateView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
    ), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('blog:password_change_done'),
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html',
    ), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('blog:password_reset_done'),
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy(
             'blog:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
    ), name='password_reset_complete'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', include(auth_urls)),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', include(profile_urls)),
    path('posts/', include(post_urls)),
    path('category/', include(category_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

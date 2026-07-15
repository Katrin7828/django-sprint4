from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name: str = 'blog'

urlpatterns: list = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('create/', views.create_post, name='create_post'),
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/toggle-publish/', views.toggle_publish,
         name='toggle_publish'),
    path('test-email/', views.test_email, name='test_email'),
    path('posts/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

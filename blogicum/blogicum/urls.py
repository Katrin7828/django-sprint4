from django.urls import include, path
from django.contrib import admin
from django.conf.urls import handler404, handler500, handler403
from django.shortcuts import render

from users.views import user_profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('profile/<str:username>/', user_profile, name='profile'),
]

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
handler403 = 'django.views.defaults.permission_denied'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'pages/403.html', status=403)

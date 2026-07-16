from django.urls import include, path
from django.contrib import admin
from django.conf.urls import handler404, handler500, handler403
from django.shortcuts import render


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
handler403 = 'pages.views.permission_denied'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('users.urls', namespace='users')),
]


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'pages/403csrf.html', status=403)

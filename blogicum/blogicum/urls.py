from django.urls import include, path
from django.contrib import admin
from django.shortcuts import render
from pages.views import (
    PageNotFoundView,
    ServerErrorView,
    PermissionDeniedView,
    CsrfFailureView,
)


handler404 = PageNotFoundView.as_view()
handler500 = ServerErrorView.as_view()
handler403 = PermissionDeniedView.as_view()
handler403_csrf = CsrfFailureView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('users.urls', namespace='users')),
]

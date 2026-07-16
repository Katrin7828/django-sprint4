from django.urls import include, path
from django.contrib import admin

from pages.views import (
    PageNotFoundView,
    PermissionDeniedView,
)

handler404 = PageNotFoundView.as_view()
handler500 = 'pages.views.server_error'
handler403 = PermissionDeniedView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('users.urls', namespace='users')),
]

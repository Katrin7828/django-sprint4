from django.urls import include, path
from django.contrib import admin
from django.conf.urls import handler404, handler500, handler403


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls', namespace='users')),
]

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
handler403 = 'django.views.defaults.permission_denied'

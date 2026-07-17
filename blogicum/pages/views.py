from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


class ContactView(TemplateView):
    template_name = 'pages/contact.html'


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Обработчик ошибки 500."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Обработчик ошибки CSRF."""
    return render(request, 'pages/403csrf.html', status=403)


def permission_denied(request, exception):
    """Обработчик ошибки 403."""
    return render(request, 'pages/403.html', status=403)

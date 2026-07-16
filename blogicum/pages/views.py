from django.views.generic import TemplateView
from django.shortcuts import render

class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


class ContactView(TemplateView):
    template_name = 'pages/contact.html'


class PageNotFoundView(TemplateView):
    template_name = 'pages/404.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


class PermissionDeniedView(TemplateView):
    template_name = 'pages/403.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)


class CsrfFailureView(TemplateView):
    template_name = 'pages/403_csrf.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)

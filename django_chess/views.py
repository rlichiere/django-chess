from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from forms import RegistrationForm
from utils import user_utils


class DocumentationView(TemplateView):
    template_name = 'chess_engine/documentation.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DocumentationView, self).get_context_data(**kwargs)
        context['levels_list'] = user_utils.get_levels_list(add_bonuses=True)
        return context


class RegisterView(TemplateView):
    template_name = 'chess_engine/register.html'
    registration_form = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return {'context': context}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self.registration_form
        context['request'] = request

        if 'creation_error' in kwargs:
            context['creation_error'] = kwargs['creation_error']
        if 'creation_success' in kwargs:
            context['creation_success'] = kwargs['creation_success']

        template = loader.get_template(self.template_name)
        content = template.render(context, request=request)
        return HttpResponse(content)

    def post(self, request, *args, **kwargs):
        form = self.registration_form(request.POST)
        if form.is_valid():

            if User.objects.filter(username=request.POST['username']).count() != 0:
                kwargs['creation_error'] = 'Username already exists.'
                return self.get(request, *args, **kwargs)
            if User.objects.filter(email=request.POST['email']).count() != 0:
                kwargs['creation_error'] = 'Email already used.'
                return self.get(request, *args, **kwargs)

            success, details = form.execute()
            if not success:
                kwargs['creation_error'] = details
                return self.get(request, *args, **kwargs)
            kwargs['creation_success'] = 'Account created.'
            return self.get(request, *args, **kwargs)

        kwargs['creation_error'] = form.errors
        return self.get(request, *args, **kwargs)

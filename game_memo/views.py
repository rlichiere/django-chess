from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'game_memo/game.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        return {'context': context}

    def get(self, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        if not context:
            return HttpResponseRedirect(reverse('login'))
        return super(HomeView, self).get(*args, **kwargs)

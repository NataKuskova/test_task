from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from search_engine.forms import *
from django.shortcuts import redirect
import logging


logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)


class SearchView(FormView):
    template_name = 'index.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.save(self.request.LANGUAGE_CODE)
        if data:
            self.request.session['mail'] = data['mail']
            return redirect('result')
        return False


class ResultView(TemplateView):
    template_name = 'result.html'


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

        data = form.save()
        if data:

            # return redirect('result', {'mail': data['mail']})
            return render(self.request, 'result.html',
                          {'mail': data['mail']})
        return False

# class ResultView(TemplateView):
#
#     def get(self, request, *args, **kwargs):
#
#         return render(request, 'result.html',
#                       {'mail': request['mail']})


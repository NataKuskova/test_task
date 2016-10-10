from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from search_engine.forms import *
from django.core.mail import send_mail
from django.shortcuts import redirect
import logging


FORMAT = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s ' \
         u'[%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename=u'logs.log')


class SearchView(FormView):
    template_name = 'index.html'
    form_class = SearchForm

    def form_valid(self, form):

        data = form.save()
        if data:
            results = '<h1>Результаты по запросу "%s"</h1>' \
                      '<p>Найдено в книге "%s", части "%s", ' \
                      'разделе "%s", главе "%s", на странице %d.</p>' \
                      % (data['text'], data['page'].book,
                         data['page'].part_name,
                         data['page'].section_name,
                         data['page'].chapter_name,
                         data['page'].number)
            send_mail(
                'Результаты поиска.',
                results,
                'natasha.kuskova@gmail.com',
                [data['mail']],
                fail_silently=False,
                html_message=results
            )
            logging.info('Message sent successfully.')
            # return redirect('result', {'mail': data['mail']})
            return render(self.request, 'result.html',
                          {'mail': data['mail']})

# class ResultView(TemplateView):
#
#     def get(self, request, *args, **kwargs):
#
#         return render(request, 'result.html',
#                       {'mail': request['mail']})


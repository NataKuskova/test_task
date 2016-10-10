from django import forms
from search_engine.models import *
import logging


FORMAT = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s ' \
         u'[%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename=u'logs.log')


class SearchForm(forms.Form):
    # class Meta:
    #     widgets = {
    #         'text': forms.TextInput(attrs=
    #                                 {'placeholder':
    #                                  'Что мы будем искать в книгах?'}),
    #         'mail': forms.Textarea(
    #             attrs={'placeholder':
    #                    'Ваш e-mail для получения '
    #                    'результатов поиска'}),
    #     }
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Что мы будем искать в книгах?'}))
    mail = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ваш e-mail для получения результатов поиска'}), max_length=100, required=True)

    def save(self):
        text = self.data.get('text', None)
        mail = self.data.get('mail', None)
        if text is not None and mail is not None:
            page = Page.objects.get_page(text)
            logging.info('Result found in the database.')
            return {'text': text,
                    'page': page,
                    'mail': mail}
        logging.info('Text or email value are empty.')
        return False



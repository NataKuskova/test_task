from django import forms
from search_engine.models import *
import logging
from django.core.mail import send_mail
from django.template.response import SimpleTemplateResponse


logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)


class SearchForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Что мы будем искать в книгах?'}))
    mail = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ваш e-mail для получения результатов поиска'}), max_length=100, required=True)

    def save(self):
        text = self.data.get('text', None)
        mail = self.data.get('mail', None)
        if text is not None and mail is not None:
            page = Page.objects.get_page(text)
            logger.info('Result found in the database.')
            message = SimpleTemplateResponse('message.html',
                                             {'text': text,
                                              'page': page},
                                             content_type='text/html; '
                                                          'charset="utf-8"')
            message.render()
            try:
                send_mail(
                    'Результаты поиска.',
                    message.content.decode('utf-8'),
                    'natasha.kuskova@gmail.com',
                    [mail],
                    fail_silently=False,
                    html_message=message.content.decode('utf-8')
                )
                logger.info('Message sent successfully.')
                return {'mail': mail}
            except:
                logger.error('Something went wrong. Message not sent.')
                return False
        logger.error('Text or email value are empty.')
        return False



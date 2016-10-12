from django import forms
import logging
from django.utils.translation import ugettext_lazy as _
from search_engine.tasks import send_message


logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)


class SearchForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Что мы будем искать в книгах?')}))
    mail = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': _('Ваш e-mail для получения результатов поиска')}),
                            max_length=100, required=True)

    def save(self, lang):
        text = self.data.get('text', None)
        mail = self.data.get('mail', None)
        if text is not None and mail is not None:
            # if send_message.apply_async(args=[text, mail], soft_time_limit=0.002):

            if send_message.delay(text, mail, lang):
                return {'mail': mail}
        logger.error('Text or email value are empty.')
        return False



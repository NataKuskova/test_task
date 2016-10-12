from django import forms
import logging
from django.utils.translation import ugettext_lazy as _
from search_engine.tasks import search


logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)


class SearchForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Что мы будем искать в книгах?')}),
        required=True)
    mail = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': _('Ваш e-mail для получения результатов поиска')}),
                            max_length=100, required=True)
    time = forms.FloatField(required=True, min_value=0.5)

    def save(self, lang):
        text = self.data.get('text', None)
        mail = self.data.get('mail', None)
        time = self.data.get('time', None)
        if text is not None and mail is not None\
                and time is not None:
            if search.apply_async(args=[text, mail, lang],
                                  soft_time_limit=float(time)):
                return {'mail': mail}
        logger.error('Text or email value are empty.')
        return False



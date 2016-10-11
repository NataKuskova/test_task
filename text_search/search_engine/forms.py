from django import forms
import logging
from search_engine.tasks import send_message


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
            if send_message.apply_async(args=[text, mail], soft_time_limit=0.002):
                return {'mail': mail}
        logger.error('Text or email value are empty.')
        return False



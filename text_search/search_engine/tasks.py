from __future__ import absolute_import
from celery import shared_task
from celery import Celery
import logging
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template.response import SimpleTemplateResponse
from celery.exceptions import SoftTimeLimitExceeded
from time import time
from django.utils.translation import activate, ugettext_lazy as _
from search_engine.models import *

logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)


def send(text, mail, page, lang):
    subject = _('Результаты поиска.')
    from_email = 'natasha.kuskova@gmail.com'
    activate(lang)
    message = SimpleTemplateResponse('message.html',
                                     {'text': text,
                                      'page': page},
                                     content_type='text/html; '
                                                  'charset="utf-8"')
    message.render()
    try:
        send_mail(
            subject,
            message.content.decode('utf-8'),
            from_email,
            [mail],
            fail_silently=False,
            html_message=message.content.decode('utf-8')
        )
        logger.info('Message sent successfully.')
        return True
    except SMTPException:
        logger.error('SMTPException. Message not sent.')
        return False



@shared_task
def search(text, mail, lang):
    page = []
    start_time = time()
    end_time = None
    try:
        rows = 0
        while True:
            result = Page.objects.get_page(text, rows)
            if not result:
                break
            page.extend(result)
            global end_time
            end_time = time()
            all_time = end_time - start_time
            logger.info('The result found in the database in {} seconds.'.format(all_time))
            rows += 2
        if page:
            return send(text, mail, page, lang)
        return False

    except SoftTimeLimitExceeded:
        logger.error('SoftTimeLimitExceeded.')
        if page:
            return send(text, mail, page, lang)
        return False




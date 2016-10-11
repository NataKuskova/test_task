from __future__ import absolute_import
from celery import shared_task
from celery import Celery
import logging
from django.core.mail import send_mail
from django.template.response import SimpleTemplateResponse
from celery.exceptions import SoftTimeLimitExceeded
from time import time
from search_engine.models import *

logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)

# celery = Celery('tasks', broker='amqp://guest@localhost//')


@shared_task
def send_message(text, mail):
    page = []
    message = SimpleTemplateResponse('message.html',
                                     {'text': text,
                                      'page': page},
                                     content_type='text/html; '
                                                  'charset="utf-8"')
    message.render()
    subject = 'Результаты поиска.'
    start_time = time()
    from_email = 'natasha.kuskova@gmail.com'
    try:
        page.extend(Page.objects.get_page(text))
        end_time = time()
        all_time = end_time - start_time
        logger.info('The result found in the database in {} seconds.'.format(all_time))

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
        except:
            logger.error('Something went wrong. Message not sent.')
            return False

    except SoftTimeLimitExceeded:
        logger.error('SoftTimeLimitExceeded.')
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
        except:
            logger.error('Something went wrong. Message not sent.')
            return False




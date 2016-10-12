from django.conf.urls import url
from search_engine.views import *


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='index'),
    url(r'^result/$', ResultView.as_view(), name='result'),
]

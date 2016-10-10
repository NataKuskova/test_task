from django.conf.urls import url
from search_engine.views import *


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='index'),
    # url(r'^result/(?P<mail>\w+)$', ResultView.as_view(), name='result'),
]

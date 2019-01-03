from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.word, name='word_stat'),
    url(r'^(?P<author_slug>[-\w]+)$', views.word, name='author_word_stat'),
]
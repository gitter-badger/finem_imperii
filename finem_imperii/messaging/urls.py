from django.conf.urls import url

from messaging.views import mark_all_read, messages_list, home, compose, mark_read, mark_favourite, favourites_list, \
    sent_list

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^read/(?P<receiver_id>[0-9]+)$', mark_read, name='mark_read'),
    url(r'^favourite/(?P<receiver_id>[0-9]+)$', mark_favourite, name='mark_favourite'),
    url(r'^read_all$', mark_all_read, name='mark_all_read'),
    url(r'^all$', messages_list, name='messages_list'),
    url(r'^favourites$', favourites_list, name='favourites'),
    url(r'^sent', sent_list, name='sent'),
    url(r'^compose$', compose, name='compose'),
    url(r'^compose/character/(?P<character_id>[0-9]+)$', compose, name='compose_character'),
    url(r'^favourite/character/(?P<character_id>[0-9]+)$', compose, name='favourite_character'),
    url(r'^unfavourite/character/(?P<character_id>[0-9]+)$', compose, name='unfavourite_character'),
]

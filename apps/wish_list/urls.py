from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'process$', views.process),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^create_item', views.create_item),
    url(r'^add/(?P<item_id>\d+)$', views.add),
    url(r'^remove/(?P<item_id>\d+)$', views.remove),
    url(r'^show/(?P<item_id>\d+)$', views.show),
    url(r'^logout$', views.logout),
]
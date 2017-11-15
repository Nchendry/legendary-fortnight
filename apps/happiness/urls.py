from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^add$', views.add),
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^addtolist$', views.addtolist),
]
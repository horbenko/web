from django.conf.urls import url
from django.http import HttpResponseRedirect

from .views import PostCreate, PostUpdate, PostDelete, ProfileView

app_name = 'api'

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('new/'), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', PostUpdate.as_view(), name='update'),
    url(r'^new/$', PostCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/delete/$', PostDelete.as_view(), name='delete'),

    # API
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]

"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from api.auth_views import RegisterView
from tastypie.api import Api

from api.api.resources import UserResource ,PostResource
from api.auth_views import RegisterView


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(PostResource())

urlpatterns = [
    # Root url.
    url(r'^$', lambda r: HttpResponseRedirect('posts/')),

    # Admin
    url(r'^admin/', admin.site.urls),

    # Registration
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {"next_page": reverse_lazy('login')}, name='logout'),
    url('^register/', RegisterView.as_view(), name='register'),

    # Api
    url(r'^posts/', include('api.urls', namespace="post")),
    url(r'^api/', include(v1_api.urls)),
]
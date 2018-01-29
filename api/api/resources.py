from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization

from ..models import Post
from .authorization import UserObjectsOnlyAuthorization


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        resource_name = 'user'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }


class PostResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        queryset = Post.objects.all()
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

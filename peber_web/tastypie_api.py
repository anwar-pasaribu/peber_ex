# coding=utf-8
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.constants import ALL
from tastypie import fields
from tastypie.authorization import Authorization

from peber_web.models import News_Source
from peber_web.models import News
from peber_web.models import UserDesc


# Kelas utk django.user
class UserResource(ModelResource):
	class Meta(object):
		queryset = User.objects.all()
		fields = ['id', 'username', 'first_name', 'last_name', 'email', ]
		resource_name = 'user'
		filtering = {
			'username': ALL,  # http://127.0.0.1:8000/peber_web/api/v1/user/?username=Pasaribu
		}


class NewsSourceResource(ModelResource):
	"""Web service untuk menyediakan API peber.peber_web_news_source"""

	class Meta(object):
		queryset = News_Source.objects.all()
		resource_name = 'news_source'  # dipakai di url. ex: /api/news_source/?format=json
		authorization = Authorization()
		filtering = {  # Fields yang diizinkan untuk diakses News
			'id': ALL,
			'source_category': ALL,
		}


class UserDescResourceApi(ModelResource):
	user = fields.OneToOneField(UserResource, 'user', full=True)
	news_choices = fields.ManyToManyField(NewsSourceResource, 'news_choices', full=True)

	class Meta(object):
		queryset = UserDesc.objects.all()
		authorization = Authorization()
		resource_name = 'user_desc'
		filtering = {
			'user': ALL_WITH_RELATIONS,
		}


class NewsResource(ModelResource):
	"""Web service untuk menyediakan API peber.peber_web_news"""
	news_corp = fields.ForeignKey(NewsSourceResource, 'news_corp', full=True)

	class Meta(object):
		queryset = News.objects.all()
		resource_name = 'news'  # dipakai di url. ex: /api/news/?format=json
		filtering = {  # Field yang boleh dipakai sebagai filter
			'news_corp': ALL_WITH_RELATIONS,
		}

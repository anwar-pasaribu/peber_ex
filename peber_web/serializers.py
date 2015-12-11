# coding=utf-8
"""
Fungsi untuk membuat REST API menggunakan DRF (Django REST Framewok)
"""
from django.contrib.auth.models import User
from rest_framework import serializers

# Model dalam aplikasi
from peber_web.models import News_Source, News, UserDesc

# Model untuk Django Celery
from djcelery.models import PeriodicTask


# API untuk django celery
class PeriodicTaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = PeriodicTask
		# depth = 1
		fields = ('id', 'name', 'task', 'args', 'crontab', 'enabled')


# Testing utk DRF
# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	# userdescs = serializers.HyperlinkedRelatedField(queryset=UserDesc.objects.all(), view_name='userdesc-detail', many=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name')


class NewsSourceSerializer(serializers.ModelSerializer):
	# Semua berita yg menggunakan id ns ini.
	# news_sources = serializers.PrimaryKeyRelatedField(many=True, queryset=News.objects.all())
	class Meta:
		model = News_Source
		fields = ('id', 'source_publisher', 'source_category', 'source_url')


###################################################
# Peber News
class NewsSerializer(serializers.ModelSerializer):
	news_corp = NewsSourceSerializer()
	class Meta:
		model = News
		fields = ('id', 'news_url', 'news_title', 'news_content', 'news_summary', 'news_pub_date', 'news_image_hero', 'news_corp')

class UserDescSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	news_choices = NewsSourceSerializer(many=True)
	class Meta:
		model = UserDesc
		fields = ('id', 'user', 'news_choices', 'bio', 'profile_pict')

class UpdateUserDescSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserDesc
		# depth = 1
		# fields = ('id', 'user', 'news_choices', 'bio', 'profile_pict')

	# def update(self, instance, validated_data):

	# 	print "News choices: %s " % self.get('news_choices')
		
	# 	# news_choices = validated_data.get('news_choices', instance.news_choices)
	# 	instance.news_choices = validated_data.get('news_choices', instance.news_choices)
	# 	instance.user = validated_data.get('user', instance.user)
	# 	instance.bio = validated_data.get('bio', instance.bio)
		

	# 	return instance
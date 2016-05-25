# coding=utf-8
from django.conf.urls import url

from peber_web import views


urlpatterns = [
	# /peber_web/
	url(r'^$', views.index, name='index'),  # URL spesifik utk aplikasi peber_web
	# /peber_web/<id_berita>
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

	# /peber_web/add_news_source/
	url(r'^add_news_source/$', views.add_news_source, name="add_news_source"),
	# peber_web/edit_news_source/<news_source_id>
	url(r'^edit_news_source/(?P<news_source_id>[0-9]+)/$', views.edit_news_source, name='edit_news_source'),
	# /peber_web/news_source_detail/<news_source_id>
	url(r'^news_source_detail/(?P<news_source_id>[0-9]+)/$', views.news_source_detail, name='news_source_detail'),

	# news source page with media list.
	url(r'^news_sources/$', views.news_source_page, name='news_source_page'),
	# Show news based on certain news_source id
	url(r'^news_sources/(?P<news_source_id>[0-9]+)/$', views.news_category, name='news_category'),

	# User peber_web (peber application)
	# /add_peber_web_user/
	url(r'^add_peber_web_user/$', views.add_peber_web_user, name="add_peber_web_user"),
	# /peber_web/user_detail/<id_user>
	url(r'^user_detail/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_detail'),

	# URL utk parser "peber_web/rss_feed_parser/"
	url(r'^rss_feed_parser/$', views.rss_feed_parser, name="rss_feed_parser"),

	# Percobaan utk session dan cookie
	# ex: peber_web/language/en-gb
	url(r'^language/(?P<language>[a-z\-]+)/$', views.language, name='language'),

	# Hasil evaluasi intrinsic
	url(r'^summary_eval/$', views.summary_eval, name='summary_eval'),

	# Generate News Terms
	url(r'^generate_terms/$', views.generate_terms, name='generate_terms'),


	# Untuk autentikasi peber_ex (parent project)
	url(r'^account/login/$', views.login, name='login'),
	url(r'^account/auth/$', views.auth_view, name='auth_view'),
	url(r'^account/logout/$', views.logout, name='logout'),
	url(r'^account/loggedin/$', views.loggedin, name='loggedin'),
	url(r'^account/invalid/$', views.invalid_login, name='invalid_login'),

	# Untuk daftar member
	url(r'^account/register/$', views.register_user, name='register_user'),
	url(r'^account/register_success/$', views.register_success, name='register_success'),
]
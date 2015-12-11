# coding=utf-8
from django.shortcuts import get_object_or_404, get_list_or_404, render  # Pengganti  loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse  # Redirect setelah submit form
from django.core.urlresolvers import reverse  # Redirect juga
from django.views import generic
from djcelery.models import PeriodicTask

from .models import UserDesc, News, News_Source  # Model
from .forms import News_SourceForm, Peber_WebUserForm, MyRegistrationForm  # Form


# Keperluan utk login
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf

# Modul untuk keperluan merging querysets
from django.db.models import Q
from functools import reduce

# Akses RSS Parser
from peber_web.function.database_access import DatabaseAccess
# Utk multi processing

# Celery tasks
from peber_web.tasks import parse_all_news_feed_task

# DRF Needs (18 Nop 2015)
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from peber_web.serializers import UserSerializer, NewsSourceSerializer, NewsSerializer, \
	UserDescSerializer, UpdateUserDescSerializer, PeriodicTaskSerializer

dbs = DatabaseAccess()


# Halaman index (peber_web).
# @login_required(login_url='peber_web:login')
def index(request):
	# get user admin yg aktif
	usr = request.user.get_username()

	# setup for session and cookies
	langua = 'en-gb'
	session_language = 'en-gb'

	# Setup for session and cookies
	if 'lang' in request.COOKIES:
		langua = request.COOKIES['lang']

	if 'lang' in request.session:
		session_language = request.session['lang']

	# Get all news from db
	all_news = dbs.get_all_news()  # Sort mulai tanggal terbaru

	all_news_source = dbs.get_all_news_source()

	# Fetch data from db and limit to only the first fifty
	user_list = UserDesc.objects.all()[:50]

	context = {
		'user_list': user_list,
		'news_sources': all_news_source,
		'language': langua,
		'session_language': session_language,
		'all_news': all_news[:15],
		'all_news_size': len(all_news),
		'logged_user': usr
	}

	# Untuk mengirim token csrf ke template
	context.update(csrf(request))

	return render(request, 'peber_web/index.html', context)


# Test class utk simpan data jumlah berita
class NewsCounting(object):
	def __init__(self, ns_id, s_name, s_url, n_num):
		self.ns_id = ns_id
		self.source_name = s_name
		self.source_url = s_url
		self.news_num = n_num


def news_category(request, news_source_id):
	"""
	Menampilkan semua News dengan ID News Source yang diberikan.
	"""
	# get user admin yg aktif
	usr = request.user.get_username()

	# setup for session and cookies
	langua = 'en-gb'
	session_language = 'en-gb'

	# Setup for session and cookies
	if 'lang' in request.COOKIES:
		langua = request.COOKIES['lang']

	if 'lang' in request.session:
		session_language = request.session['lang']

	all_news_source = dbs.get_all_news_source()

	context = {
		'news_sources': all_news_source,
		'language': langua,
		'session_language': session_language,
		'all_news_size': len(dbs.get_all_news().all()),
		'logged_user': usr
	}

	# Untuk mengirim token csrf ke template
	context.update(csrf(request))

	# Jika ada news_source_id buka list berita (news)
	# yang berhubungan dengan news_source_id tersebut
	news_data = get_list_or_404(News.objects.filter(news_corp_id=news_source_id))
	context['news_data'] = news_data
	context['current_ns'] = '(%d) %s - %s' % (len(news_data), news_data[0].news_corp.source_category, news_data[0].news_corp.source_publisher)
	return render(request, 'peber_web/news_source_page.html', context)


def news_source_page(request):
	"""
	Menampilkan semua News Source dan jumlah berita dengan kategori tersebut.
	"""
	# get user admin yg aktif
	usr = request.user.get_username()

	# setup for session and cookies
	langua = 'en-gb'
	session_language = 'en-gb'

	# Setup for session and cookies
	if 'lang' in request.COOKIES:
		langua = request.COOKIES['lang']

	if 'lang' in request.session:
		session_language = request.session['lang']

	# Get all news from db
	all_news = dbs.get_all_news()  # Sort mulai tanggal terbaru

	all_news_source = dbs.get_all_news_source()

	# Membuat object baru yang menyimpan
	# Sumber Berita dan jumlah berita terkait
	news_count = []
	for i in all_news_source:
		s_name = '{0} ({1})'.format(i.source_publisher, i.source_category)
		n_num = len(News.objects.filter(news_corp_id=i.id))

		news_count.append(NewsCounting(i.id, s_name, i.source_url, n_num))

	print news_count[0].source_name

	context = {
		'news_count': news_count,
		'news_sources': all_news_source,
		'language': langua,
		'session_language': session_language,
		'all_news': all_news[:25],
		'all_news_size': len(all_news),
		'logged_user': usr
	}

	# Untuk mengirim token csrf ke template
	context.update(csrf(request))

	return render(request, 'peber_web/news_source_page.html', context)


# Register user
def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('peber_web/login.html', c)


def auth_view(request):
	# Form dibuat hordcode utk username dan password pada login.html
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')

	user = auth.authenticate(username=username, password=password)  # memeriksa database.table auth_user

	if user is not None:
		auth.login(request, user)  # Register user dalam session sudah login

		# Metode redirect yang dianjurkan jika memakai fungsi post.
		return HttpResponseRedirect(reverse('peber_web:loggedin'))
	else:
		return HttpResponseRedirect(reverse('peber_web:invalid_login'))


def loggedin(request):
	return render_to_response('peber_web/loggedin.html', {'full_name': request.user.username})


def invalid_login(request):
	return render_to_response('peber_web/invalid_login.html')


def logout(request):
	auth.logout(request)
	return render_to_response('peber_web/logout.html')


def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)  # Kelas extended UserCreationForm

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('peber_web:register_success'))

	args = {}
	args.update(csrf(request))
	args['forms'] = MyRegistrationForm()

	return render_to_response('peber_web/register.html', args)


def register_success(request):
	return render_to_response('peber_web/register_success.html')


def language(request, lang='en-gb'):
	"""Untuk demo penggunaan session dan cookies"""
	response = HttpResponse('Setting lang to :{0}'.format(lang))

	# Memasukkan var ke cookie
	response.set_cookie('lang', lang)

	# set session
	request.session['lang'] = lang

	return response


# Versi generic view
# untuk menampilkan detail berita
class DetailView(generic.DetailView):
	model = News
	template_name = 'peber_web/detail.html'
	context_object_name = 'news_data'


# versi normal (yet i like it)
# def detail(request, id_berita):
# news_list = get_object_or_404(News, pk=id_berita) #Mendapatkan berita dengan filter
# return render(request, 'peber_web/detail.html', {'news_list': news_list})


# Edit news source [Belum ready]
def edit_news_source(request, news_source_id):
	global news_s

	if news_source_id:
		news_s = News_Source.objects.get(pk=news_source_id)

	if request.method == 'GET':
		form = News_SourceForm(news_s)
	else:
		form = News_SourceForm(request.POST)

		if form.is_valid():
			form.save()

			return HttpResponseRedirect(reverse('peber_web:index'))

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render(request, 'peber_web/add_news_source.html', args)


# Detail lengkap tentang news_source
def news_source_detail(request, news_source_id):
	news_source_data = get_object_or_404(News_Source, pk=news_source_id)
	return render(request, 'peber_web/news_source_detail.html', {'news_source_data': news_source_data})


# Versi Mike Hibbert (simple)
def add_news_source(request):
	if request.method == 'GET':
		form = News_SourceForm()
	else:
		form = News_SourceForm(request.POST)

		if form.is_valid():
			form.save()

			return HttpResponseRedirect(reverse('peber_web:index'))

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render(request, 'peber_web/add_news_source.html', args)


# Tambah user (peber_web)
# dan cara upload file.


def add_peber_web_user(request):
	if request.method == 'GET':
		form = Peber_WebUserForm()
	else:
		form = Peber_WebUserForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()

			return HttpResponseRedirect(reverse('peber_web:index'))

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render(request, 'peber_web/add_peber_web_user.html', args)


class UserDetailView(generic.DetailView):
	model = UserDesc
	template_name = 'peber_web/user_detail.html'
	context_object_name = 'user_dict'


# mencari dengan AJAX
def search_titles(request):
	if request.POST:
		search_text = request.POST['search_text']
	else:
		search_text = ''

	print('Search text:', search_text)

	# Ambil data berdasarkan judul
	news_res = News.objects.filter(news_title=search_text)

	return render_to_response('peber_web/ajax_search.html', {'news_res': news_res})


# Parsing RSS
def rss_feed_parser(request):
	# Parse RSS Feed
	"""
	Untuk menjalankan parse_all_news_feed_task
	:param request:
	:return:
	"""
	db_access = DatabaseAccess()

	# all_news_source = dbs.get_all_news_source()

	# print("News Res ({1}):{0}".format(all_news_source, len(all_news_source)))

	# for news_source in all_news_source:
	# 	parse_news_feed_task.delay(news_source.id, news_source.source_url)

	# Semua data berita
	all_news = db_access.get_all_news()[:10]

	# Parse RS Feed
	parse_all_news_feed_task.delay()

	return render_to_response('peber_web/news.html', {'news_data': all_news})


##########################################################################################
# DRF (18 Nop)
# Bagian untuk menyediakan API
# News Source API View

# API for djcelery model
class PeriodicTaskViewSet(viewsets.ModelViewSet):
	queryset = PeriodicTask.objects.all()
	serializer_class = PeriodicTaskSerializer

# Pagination
# noinspection PyAbstractClass
class StandardResultsSetPagination(PageNumberPagination):
	page_size = 100
	page_size_query_param = 'page_size'
	max_page_size = 1000


# News Source API View
class NewsSourceViewSet(viewsets.ModelViewSet):
	"""
	View untuk menyediakan data News Source dengan 
	ukuran data per halaman 100 data.
	ModelViewSet, berarti CRUD pada model diizinkan.
	"""
	pagination_class = StandardResultsSetPagination
	serializer_class = NewsSourceSerializer

	# Custom query 
	def get_queryset(self):
		# Default queryset
		queryset = News_Source.objects.all()

		data = self.request.query_params
		is_distinct = data.get('distinct', None)  # Param untuk menetukan distinct atau tidak.
		categories = data.get('category', None)  # Param untuk filter berdasarkan kategori

		if is_distinct is not None:
			# Ambil data setelah digambungkan berdasarkan source_category
			queryset = News_Source.objects.distinct('source_category')

		elif categories is not None:
			# Filter data hanya kategory tertentu
			categories_num = len(categories.split(','))
			if categories_num != 0:  # Jika kategori >= 1
				categories = categories.split(',')
				queryset = News_Source.objects.filter(
					reduce(lambda x, y: x | y, [Q(source_category=cat) for cat in categories]))
			elif categories_num == 0:  # Tidak val pada params
				queryset = News_Source.objects.filter(source_category=categories)

		return queryset.order_by('source_category')  # Urutkan berdasarkan kategori berita


# News API View
class NewsViewSet(viewsets.ModelViewSet):
	# queryset = News.objects.all()
	serializer_class = NewsSerializer
	# filter_backends = (filters.DjangoFilterBackend,)
	# filter_fields = ('news_title', 'news_corp__source_category')

	# Custom query untuk filter berdasarkan kategori berita.
	def get_queryset(self):
		queryset = News.objects.all()

		data = self.request.query_params
		categories = data.get('news_category', None)
		title = data.get('title', None)

		# Dapatkan berita berdasarkan kategory
		if categories is not None:
			categories_num = len(categories.split(','))
			if categories_num != 0:  # Jika kategori >= 2
				categories = categories.split(',')
				queryset = News.objects.filter(
					reduce(lambda x, y: x | y, [Q(news_corp__source_category=cat) for cat in categories]))
			elif categories_num == 0:  # Hanya ada satu kategori
				queryset = News.objects.filter(news_corp__source_category=categories)

		# Filter berita dengan judul
		if title is not None:
			queryset = News.objects.filter(news_title__icontains=title)

		return queryset


# Admin User
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API untuk Django Model User
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer


# User Desc
class UserDescViewSet(viewsets.ModelViewSet):
	""" 
	API untuk model User_Desc.
	"""
	# Autentikasi User Desc. Hanya bisa di edit oleh yg login.
	# permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
	queryset = UserDesc.objects.all()
	serializer_class = UserDescSerializer


# User Desc
class UpdateUserDescViewSet(viewsets.ModelViewSet):
	""" 
	API untuk model Update news_choices User_Desc.
	"""
	# Autentikasi User Desc. Hanya bisa di edit oleh yg login.
	# permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
	queryset = UserDesc.objects.all()
	serializer_class = UpdateUserDescSerializer

##########################################################################################

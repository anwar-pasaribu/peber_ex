from django.contrib import admin

# Register your models here.
from .models import UserDesc as UserDescription, News, News_Source


# Modifkasi bagaimana tampilan admin
# Untuk menyortir field
class UserAdmin(admin.ModelAdmin):
	fieldsets = [
		('Personal data', {'fields': ['bio',]})
	]

	# Untuk mengatur tampilan field
	list_display = ('bio',)

# User Desc Amin View
class UserDescAdmin(admin.ModelAdmin):
	list_display = ('thumbnail', 'id', 'username', 'favorites', 'bio')
	ordering = ('id', )

	def username(self, obj):
		return '%s' % obj.user.username

	def favorites(self, obj):
		if obj.news_choices: 
			return ''.join('%s (%s), ' % (nc.source_publisher, nc.source_category) for nc in obj.news_choices.all()).rsplit(',', 1)[0]
		else:
			return "No choice."
			 

	def thumbnail(self, obj):
		if obj.profile_pict:
			return '<img src="%s" style="height: 50px; width: auto">' % (obj.profile_pict.url)
		else:
			return "no image"

	thumbnail.allow_tags = True


class NewsSourceAdmin(admin.ModelAdmin):
	list_display = ('id', 'source_publisher', 'source_category', 'source_url', 'news_count')

	def news_count(self, obj):
		return '{0} Berita'.format(len(News.objects.filter(news_corp__id=obj.id)))
	news_count.allow_tags = True


class NewsAdmin(admin.ModelAdmin):
	list_display = ('id', 'news_corp', 'news_title', 'news_url')
	ordering = ('-news_pub_date', )

admin.site.register(UserDescription, UserDescAdmin)
admin.site.register(News_Source, NewsSourceAdmin)
admin.site.register(News, NewsAdmin)

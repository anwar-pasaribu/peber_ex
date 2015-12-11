from django import forms
from .models import News_Source, UserDesc as User_Peber

# untuk add user
from django.contrib.auth.models import User as AdminUser
from django.contrib.auth.forms import UserCreationForm

# Modifikasi pesan
from django.utils.translation import ugettext_lazy as _


# class News_SourceForm(forms.Form):
# source_publisher = forms.CharField()
# source_category = forms.CharField(max_length=50)
# source_url = forms.CharField()

# From Mike Hibbert
class News_SourceForm(forms.ModelForm):
	class Meta:
		model = News_Source
		fields = ['source_publisher', 'source_category', 'source_url']
		# fields = '__all__' # semua fields
		# exclude = ['source_category'] # black list field
		labels = {
			'source_publisher': _('Publisher'),
		}


# form utk tambah data peber_web_user
class Peber_WebUserForm(forms.ModelForm):
	class Meta:
		model = User_Peber
		# fields = ['username', 'full_name', 'password', 'email', 'profile_pict']
		fields = '__all__'


# Kelas utk menambah form bawaan UserCreationForm
# Mike Hibbert Tutorial
class MyRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = AdminUser
		fields = ('username', 'email', 'password1', 'password2')

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.set_password(self.cleaned_data['password1'])  # Cara menyimpan password pada user admin

		# if commit:
		user.save()

		return user

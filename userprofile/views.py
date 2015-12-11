from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse  # Redirect juga
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm


@login_required(login_url='peber_web:login')
def user_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/peber_web/accounts/loggedin/')  # peber_web:loggedin
		else:
			user = request.user
			profile = user.profile
			form = UserProfileForm(instance=profile)

		args = {}
		args.update(csrf(request))

		args['form'] = form

		return render_to_response('userprofile/profile.html', args)

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from bleeps.models import UserProfile, UserProfileForm, UserAuthToken, UserAuthTokenForm

import datetime
import logging
logger = logging.getLogger(__name__)

#
# User profile
#
@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        else:
            print 'debuggery: profile form was not valid'
    else:
        print 'debuggery: it is a GET profile form request'
        form = UserProfileForm(instance=profile)
    return render_to_response(
        'registration/profile.html', 
        {'user':request.user,
         'form':form,
         'token_form':UserAuthTokenForm({'user_profile':request.user.profile})},
        context_instance=RequestContext(request))

#
# User authorization token
#
@login_required
def tokens(request):
    if request.method == 'POST':
        form = UserAuthTokenForm(request.POST)
        if form.is_valid():
            print 'debuggery: Saving an api key'
            token = form.save(commit=False)
            token.timestamp = datetime.datetime.now()
            token.token = UserAuthToken.generate_token()
            token.user_profile = request.user.profile
            form.save()
        else:
            print 'debuggery: the token form was invalid'
    elif request.method == 'GET':
        print 'debuggery: GET tokens request ignored'
        pass
    return profile(request)


def token_delete(request, token_id):
    if request.method == 'POST':
        token = get_object_or_404(UserAuthToken, pk=token_id)
        token.delete()
    return profile(request)


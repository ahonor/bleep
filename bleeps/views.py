from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from bleeps.models import Bleep, BleepForm, BleepSearchForm, CommentForm
from services.BleepService import BleepService, BleepServiceForm

import datetime
import logging
logger = logging.getLogger(__name__)



def as_paginated(request, bleep_list, max=10):
    paginator = Paginator(bleep_list, max); 
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        bleeps = paginator.page(page)
    except (EmptyPage, InvalidPage):
        bleeps = paginator.page(paginator.num_pages)
        
    return render_to_response('bleep/list.html', 
                              {'user':request.user,
                               'bleep_list': bleeps},
                              context_instance=RequestContext(request))

@login_required
def bleeps(request):
    """
    list the latest bleeps

    """
    return as_paginated(request,Bleep.objects.all().order_by('-bleep_pub_date'))
    


@login_required
def search(request):
    """
    search the bleeps

    """
    print 'debuggery: searching the bleepdom'
    form = BleepSearchForm(request.POST)
    bleep_list = []
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        print 'debuggery: keyword='+keyword
        bleep_list = Bleep.objects.filter(bleep_message__contains=keyword).order_by('-bleep_pub_date')
    return as_paginated(request, bleep_list)


@csrf_exempt
def add(request):
    """
    Add a bleep to the bleepdom

    """
    print 'debuggery: inside add function...'
    if request.method == 'POST':
        # merge the GET and POST params
        reqParams = request.POST.copy()
        reqParams.update(request.GET)
        form = BleepForm(reqParams)
        if form.is_valid():
            print 'debuggery: add form is valid'
            # Initialize the date and status            
            new_instance = form.save(commit=False)
            new_instance.bleep_status='qued'
            new_instance.bleep_pub_date = datetime.datetime.now()
            # Collect the input params
            new_instance.bleep_get_data = request.META['QUERY_STRING']
            if request.raw_post_data:
                new_instance.bleep_post_data = request.raw_post_data
            # Save the data to the model
            new_instance.save()
            if not settings.NO_AUTO_SEND_MESSAGE:
                # send it!
                print 'debuggery: Automatically sending the bleep...'
                result = BleepService.dispatch(new_instance)
            else:
                print 'debuggery: bleep is being held in queue for later processing'
            # Return to the new bleep page
            return HttpResponseRedirect('/bleeps/'+str(new_instance.id))
        else:
            logger.debug('the add form was NOT valid')
    else:
        return render_to_response('bleep/create.html', {
                'form':BleepForm(
                    initial={'bleep_status':'qued',
                             'bleep_pub_date':datetime.datetime.now()})},
                                  context_instance=RequestContext(request))        

@login_required
def show(request, bleep_id):
    """
    Dispaly bleep detail
    
    """
    b = get_object_or_404(Bleep, pk=bleep_id)
    return render_to_response('bleep/detail.html',
                              {'bleep': b, 'comment_form': CommentForm()},
                                context_instance=RequestContext(request))

@login_required
def edit(request, bleep_id):
    """
    Edit a bleep

    """
    b = get_object_or_404(Bleep, pk=bleep_id)
    return render_to_response('bleep/form.html', {
            'form': BleepForm(instance=b),
        'content_form': CommentForm(),
            'bleep': b,}, context_instance=RequestContext(request))             

@login_required
def update(request, bleep_id):
    """
    Process a bleep form update

    """
    if request.method == 'POST':
        form = BleepForm(request.POST)
        if form.is_valid():
            # Process and clean the data
            # ...
            # update the form with current bleep data
            b = Bleep.objects.get(pk=bleep_id)
            form = BleepForm(request.POST, instance=b)
            form.save()
            return HttpResponseRedirect('/bleeps/'+bleep_id)
        else:
            form = BleepForm() # Create an unbound form
    return render_to_response('bleep/form.html', {
            'form': form,
        'content_form': CommentForm()}, context_instance=RequestContext(request))

@login_required
def send(request, bleep_id):
    print 'debuggery: dispatching %s to external service' % bleep_id
    """
    Dispatch the bleep 

    """
    b = get_object_or_404(Bleep, pk=bleep_id)
    BleepService.dispatch(b)        
    # return to page
    return render_to_response('bleep/detail.html', { 'bleep': b},
                              context_instance=RequestContext(request))

@login_required
def digest(request):
    """
    Generate a digest

    """
    bleeps = Bleep.objects.all()
    # return to page
    return render_to_response('email/digest.html', { 'bleeps': bleeps},
                              context_instance=RequestContext(request))


@login_required
def comment(request, bleep_id):
    """
    Add a comment to the bleep
    """
    b = get_object_or_404(Bleep, pk=bleep_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.bleep = b
            comment.user = request.user
            if not comment.timestamp:
                comment.timestamp = datetime.datetime.now()
            form.save()
        else:
            print 'debuggery: not valid comment'
    return render_to_response('bleep/detail.html',
                              { 'bleep': b,
                                'comment_form': CommentForm(),},
                              context_instance=RequestContext(request))

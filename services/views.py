from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from services.BleepService import BleepService, BleepServiceForm
from parsers.BleepParser import BleepParser, BleepParserForm
from parsers.PyDictParser import PyDictParser

import datetime
import logging
logger = logging.getLogger(__name__)


#
# Services
#
@login_required
def list(request):
    """
    List the bleep services

    """
    services = BleepService.list()
    parsers = BleepParser.list()
    return render_to_response('services/list.html',
                              {'services_list': services,
                               'parsers_list': parsers},
                              context_instance=RequestContext(request))


@login_required
def show(request, service_type):
    """
    Show the service 

    """
    service = BleepService.get_service(service_type)
    form_class = BleepService.form_class(service_type)
    form = form_class()
    return render_to_response('services/detail.html',
                              {'service': service,
                               'form':form},
                              context_instance=RequestContext(request))
@login_required
def perform(request, service_type):
    if request.method == 'POST':
        # get the form class
        form_class = BleepService.form_class(service_type)
        form = form_class(request.POST)
        service = BleepService.get_service(service_type)
        form_dict = form.data.copy()
        if form_dict.has_key('data'):
            print 'debuggery: parsing form dictionary data...'
            parsed_dict = PyDictParser.string_to_dict(form_dict['data'])
            form_dict.update(parsed_dict)
            del form_dict['data']
        print 'calling perform()...'
        result = service.perform(form_dict)
        return render_to_response('services/detail.html',
                                      {'service': service,
                                       'result':result.get_msgs(),
                                       'form':form},
                                      context_instance=RequestContext(request))


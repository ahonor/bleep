from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import datetime
import logging
logger = logging.getLogger(__name__)


#
# Help
#
def index(request):
    """
    Show the help index

    """
    return render_to_response('help/index.html',
                              {},
                              context_instance=RequestContext(request))


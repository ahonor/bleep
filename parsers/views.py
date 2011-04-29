from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from parsers.BleepParser import BleepParser, BleepParserForm
from parsers.PyDictParser import PyDictParser

import datetime
import logging
logger = logging.getLogger(__name__)


#
# Parsers
#
@login_required
def show(request, parser_type):
    """
    Show the parser

    """
    parser = BleepParser.get_type(parser_type)
    return render_to_response('services/parser.html',
                              {'parser': parser,
                               'form':BleepParserForm()},
                              context_instance=RequestContext(request))


@login_required
def perform(request, parser_type):
    """
    Show the parser

    """    
    print 'debuggery: parser_type='+parser_type
    parser = BleepParser.get_type(parser_type)
    if request.method == 'POST':
        form = BleepParserForm(request.POST)
        if form.is_valid():

            print 'debuggery: trying out this parser: '+parser.__class__.__name__
            post_data = form.cleaned_data['post_data']
            post_dict = parser.parse_reqdata(
                request.META['QUERY_STRING'],
                post_data)
            return render_to_response('services/parser.html',
                                      {'parser': parser,
                                       'parse_result':post_dict,
                                       'form':form},
                                      context_instance=RequestContext(request))
        else:
            form = BleepParserForm()
            return render_to_response('services/parser.html',
                                      {'parser':parser, 'form':form},
                                      context_instance=RequestContext(request))

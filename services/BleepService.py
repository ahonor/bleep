__all__ = ["BleepService","BleepServiceError",]


import os
import urllib2
from django.contrib.sites.models import Site
from django.conf import settings

from parsers.BleepParser import BleepParser

class BleepServiceError(Exception):
  """
  Bleep Service exception class.

  Attributes:
      message -- explanation of the error

  """
  def __init__(self, *args):
    """
    base constructor for error type
    
    """
    Exception.__init__(self, *args)


class BleepServiceResult(object):
  """
  response
  """
  def __init__(self, *args):
    self.messages = []

  def add_msg(self, msg):
    return self.messages.append(msg)

  def get_msgs(self):
    return ",".join(self.messages)

  msgs = property(get_msgs)


from django import forms
class BleepServiceForm(forms.Form):
  """
  Form for external services
  """


class BleepService(object):
  """
  Base class for all Bleep services

  Attributes:
    service_type -- the name for this Bleep service type

  """
  def __init__(self, service_type):
    self.service_type= service_type
    self.result = BleepServiceResult()

  @classmethod
  def get_name(cls):
    return cls.__name__

  @classmethod
  def get_doc(cls):
    return cls.__doc__

  def get_result(self):
    return self.result

  @classmethod
  def get_service_type(cls):
    return False
  
  @classmethod
  def is_service_type(cls, service_type):
    return cls.get_service_type() == service_type

  PARAMS = {}
  @classmethod
  def data_keys(cls):
    """
    Returns a dictionary describing the data keys

    """
    # return an empty dictionary by default
    return dict()
  
  @classmethod
  def dispatch(cls, instance):
    """
    Dispatch the bleep to its receivers

    """
    if 'qued' == instance.bleep_status:
      try:
        print 'debuggery: looking up parser for content_type ' + instance.bleep_content_type
        parser = BleepParser.get_parser(instance.bleep_content_type)
        print 'debuggery: parser='+parser.get_name()
        target_svc = BleepService.get_service(instance.bleep_service)
        print 'debuggery: target_svc='+target_svc.get_name()
        instance.bleep_status = 'dspd'
        instance.save()
        print 'debuggery: telling service to doit...'
        result = target_svc.doit(instance, parser)
        instance.bleep_status = 'comp'
        instance.save()
        print 'debuggery: adding comment about completion...'
        instance.add_comment(result.get_msgs(),
                             cat=target_svc.get_name(), stat="completed")
        print 'debuggery: comment added.'
      except BleepServiceError as (exc):
        instance.add_comment("Service request failed. Cause: "+ str(exc))
        instance.bleep_status = 'fail'
        instance.save()
    else:
      print 'debuggery: bleep not queued. status: %s' % instance.bleep_status

  def perform(self, reqdata):
    raise BleepServiceError('the base BleepService does nothing')


  def doit(self, instance, parser):
    """
    doit -- template method calling: parse_data, perform, get_results

    """
    # Get the bleep instance data as a dictionary
    bleep_data = instance.as_dict()
    # Parse the request data into a dictionary
    parsed_reqdata = parser.parse_reqdata(
      instance.bleep_get_data, instance.bleep_post_data)
    print 'debuggery: ... dumping out parsed_reqdata'
    for key,val in parsed_reqdata.iteritems():
      print "debuggery: %s=%s" % (key,val)
    # Merge the two data sets into a shared context
    context_data = dict(bleep_data, **parsed_reqdata)
    # Perform the service request
    return self.perform(context_data)

  @classmethod
  def get_service(cls, service_type):
    """
    Factory method for BleepService subclasses

    """
    for cls in BleepService.__subclasses__():
      if cls.is_service_type(service_type):
        return cls(service_type)
    raise BleepServiceError("no service found for type: %s" % service_type)



  @classmethod
  def list(cls):
    """
    List all subclasses that implement a service

    """
    results = []
    # list anything for now
    for cls in BleepService.__subclasses__():
      results.append(cls)
    return results


  @classmethod
  def get_site_url(cls):
    """Returns fully qualified URL (no trailing slash) for the current site."""
    current_site = Site.objects.get_current()
    protocol = getattr(settings, 'MY_SITE_PROTOCOL', 'http')
    port     = getattr(settings, 'MY_SITE_PORT', '')
    url = '%s://%s' % (protocol, current_site.domain)
    if port:
        url += ':%s' % port
    return url



  @classmethod
  def form_class(cls, service_type):
    """
    Generate a new class definition for this service type

    """
    cls = BleepService.get_service(service_type)
    attrs = dict()
    attrs['service_class'] = cls
    for key,d in cls.PARAMS.iteritems():
      print 'debuggery: processing param key: ', key
      req = True if d.has_key('optional') else False
      initial = d['default'] if d.has_key('default') else None
      attrs[key] = forms.CharField(key, label=key, required=req, help_text=d['desc'],
                                   initial=initial,
                                   widget=forms.TextInput(attrs={'size':'40','class':'service_param'}))
      print 'debuggery: added form attr: ' + key
    attrs['data'] = forms.CharField('data', label='data', required=False,
                                    help_text='extra request data', widget=forms.Textarea)
    print 'debuggery: generating new form class: ' + cls.get_name()+'Form'
    form_class = type(cls.get_name()+ 'Form',
                     (BleepServiceForm,), attrs)
    return form_class





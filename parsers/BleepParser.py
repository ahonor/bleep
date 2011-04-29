__all__ = ["BleepParser","BleepParserError","BleepParserForm",]


import urllib

class BleepParserError(Exception):
  """
  Parser exception class.

  Attributes:
      message -- explanation of the error

  """

  def __init__(self, *args):
    """
    base constructor for error type
    
    """
    Exception.__init__(self, *args)



class BleepParser(object):
  """
  Base class for all Bleep parsers

  Attributes:
    content_type -- the name for this Bleep parser type

  """
  def __init__(self, content_type):
    self.content_type = content_type
    self.results = []

  @classmethod
  def get_name(cls):
    return cls.__name__

  @classmethod
  def get_doc(cls):
    return cls.__doc__

  def get_results(self):
    return self.results

  @classmethod
  def get_content_type(cls):
    return cls.content_type
  
  @classmethod
  def is_content_type(cls, content_type):
    return cls.get_content_type() == content_type


  @classmethod
  def get_parser(cls, content_type):
    """
    Factory method for BleepParser subclasses

    """
    for cls in BleepParser.__subclasses__():
      print 'debuggery: checking if %s is a parser for type %s' % (cls.__name__, content_type)
      if cls.is_content_type(content_type):
        return cls(content_type)
    raise BleepParserError("no parser found for content type: %s" % content_type)



  @classmethod
  def get_type(cls, parser_type):
    """
    Lookup parser by type name

    """
    for cls in BleepParser.__subclasses__():
      if cls.__name__ == parser_type:
        print 'debuggery: checked parser type: '+cls.__name__
        return cls(parser_type)
    raise BleepParserError("no parser found for type: %s" % parser_type)

  def parse_getparams(cls, params_string):
   """
    parse GET params into dictionary

    """
   parsed_dict = {}
   if params_string:
     for k,v in dict([(x.split('=')) for x in params_string.split('&')]).iteritems():
       parsed_dict[k] = urllib.unquote_plus(v)
   return parsed_dict


  @classmethod
  def list(cls):
    """
    List all subclasses that implement a service

    """
    results = []
    # list anything for now
    for cls in BleepParser.__subclasses__():
      results.append(cls)
    return results

from django import forms
class BleepParserForm(forms.Form):
  post_data = forms.CharField ( widget=forms.widgets.Textarea() )



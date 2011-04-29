from parsers.BleepParser import BleepParser, BleepParserError

import ast

class PyDictParser(BleepParser):
  """
  Parses python dictionary

  """

  @classmethod
  def get_content_type(cls):
    return 'application/python+dict'

  @classmethod
  def string_to_dict(cls, string):
      result = {}
      try:
          result = dict(ast.literal_eval(string))
      except:
          #raise BleepParserError
          pass
      return result
  
  def parse_reqdata(self, get_data, post_data):
    """
    parse query params and POST data into dictionary

    """
    print 'debuggery: runing parse_reqdata...'
    try:
        data_dict = PyDictParser.string_to_dict(post_data)
    except ValueError as (exc):
        raise BleepParserError(exc)
    
    # merge the query_params data
    for k,v in self.parse_getparams(get_data).iteritems():
      data_dict[k] = v
    print 'debuggery: parsed !'
    # return the dictionary data
    return data_dict








    

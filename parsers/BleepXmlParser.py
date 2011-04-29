from xml.etree.ElementTree import ElementTree, XMLParser

from parsers.BleepParser import BleepParser
from parsers.XmlDictConfig import XmlListConfig, XmlDictConfig

class BleepXmlParser(BleepParser):
  """
  Parses XML into a dictionary

  """

  @classmethod
  def get_content_type(cls):
    return 'application/xml'
  
  @classmethod
  def is_content_type(cls, content_type):
    return content_type == cls.get_content_type()

  def parse_reqdata(self, get_data, post_data):
    """
    parse query params and POST data into dictionary

    """
    print 'debuggery: runing parse_reqdata...'
    data_dict = {}
    parser = XMLParser()
    tree = parser.feed(post_data)
    root = parser.close()
    data_dict = XmlDictConfig(root)
    # merge the query_params data
    for k,v in self.parse_getparams(get_data).iteritems():
      data_dict[k] = v
    print 'debuggery: parsed !'
    # return the dictionary data
    return data_dict






    

import urllib2
from xml.etree.ElementTree import ElementTree, XMLParser

from parsers.BleepParser import BleepParser, BleepParserError

class RundeckExecutionService(BleepParser):  
  """
  Interface to rundeck-execution notifications
  """

  @classmethod
  def get_content_type(cls):
    return 'application/rundeck-execution+xml'

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
    try:
      parser.feed(post_data)
      root = parser.close()
      execElement = root.find("executions/execution")
      if not execElement:
        raise BleepParserError("Did not find executions/execution element in post data")
      data_dict['execution_id'] = execElement.attrib["id"]
      data_dict['execution_href'] = execElement.attrib["href"]
      data_dict['execution_status']= execElement.attrib["status"]
      data_dict['execution_user'] = execElement.find("user").text
      data_dict['execution_date_started']= execElement.find("date-started").text
      data_dict['execution_date_ended']= execElement.find("date-ended").text
      data_dict['execution_description']= execElement.find("description").text
      data_dict['execution_job_name']= execElement.find("job/name").text
      data_dict['execution_job_group']= execElement.find("job/group").text
      data_dict['execution_job_project']=execElement.find("job/project").text
      data_dict['execution_job_description']= execElement.find("job/description").text
    except KeyError as (keyerr):
      print "Oops! missing key error: " + str(keyerr)
    except AttributeError as (atterr):
      print "Oops! missing attribute error" + str(atterr)
    except Exception as (parserr):
      raise BleepParserError("Unexpected error when parsing post data. "
                              + "Cause: " + str(parserr))
    # merge the query_params data
    for k,v in self.parse_getparams(get_data).iteritems():
      data_dict[k] = v
    print 'debuggery: parsed !'
    # return the dictionary data
    return data_dict


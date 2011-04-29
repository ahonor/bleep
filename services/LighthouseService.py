import urllib2
import xml.etree.ElementTree

from bleeps.models import Bleep
from services.BleepService import BleepService, BleepServiceError

from parsers.XmlDictConfig import XmlListConfig, XmlDictConfig
from xml.etree.ElementTree import ElementTree, XMLParser

__all__ = ['LighthouseService',]


class LighthouseService(BleepService):
  """
  Create and update tickets in http://lighthouseapp.com 

  """
  @classmethod
  def get_service_type(cls):
    return 'lighthouse'


  PARAMS =  {
    'project':{'desc':'the project name'},
    'project_id':{'desc':'the project identifier'},
    'token': {'desc':'the auth token'},
    'ticket_id': {'desc':'the ticket identifier'},
    'title':{'desc':'the ticket title'},
    'milestone_id':{'desc':'milestone id', 'optional':True},
    'tag':{'desc':'tags list', 'optional':True},
    'assigned_user_id':{'desc':'assigned user id', 'optional':True},
    'state':{'desc':'ticket state. new, open, resolved, hold, invalid', 'optional':True},
    'body':{'desc':'ticket message body'},
    }
  

  def perform(self, reqdata):
    if not reqdata.has_key('project'):
      raise BleepServiceError("missing required param: project")
    if not reqdata.has_key('project_id'):
      raise BleepServiceError("missing required param: project_id")
    if not reqdata.has_key('token'):
      raise BleepServiceError("missing required param: token")    
    if reqdata['ticket_id']:
      # update the ticket
      self._update_ticket(reqdata)
    else:
      # create the ticket
      self._create_ticket(reqdata)
    return self.get_result()



  def _update_ticket(self, reqdata):
    print 'debuggery: updating ticket ...'
    url = "http://%s.lighthouseapp.com/projects/%s/tickets/%s.xml" % (
      reqdata['project'],
      reqdata['project_id'],
      reqdata['ticket_id'])
    ticket = xml.etree.ElementTree.Element("ticket")
    if reqdata.has_key('assigned_user_id') and reqdata['assigned_user_id']:
      subel = xml.etree.ElementTree.SubElement(ticket, "assigned-user-id")
      subel.text = reqdata['assigned_user_id']
    if reqdata.has_key('body') and reqdata['body']:
      subel = xml.etree.ElementTree.SubElement(ticket, "body")
      subel.text = reqdata['body']      
    if reqdata.has_key('state') and reqdata['state']:
      subel = xml.etree.ElementTree.SubElement(ticket, "state")
      subel.text = reqdata['state']
    if reqdata.has_key('title') and reqdata['title']:
      subel = xml.etree.ElementTree.SubElement(ticket, "title")
      subel.text = reqdata['title']
    data = xml.etree.ElementTree.tostring(ticket)
    response = self._submit_request(url, reqdata['token'], data, method='PUT')
    data = response.read()
    print 'data: '+data
    self.get_result().add_msg('updated ticket %s!' % reqdata['ticket_id'])
    return self.get_result()


  def _create_ticket(self, reqdata):
    print 'debuggery: creating a new ticket ...'
    url = "http://%s.lighthouseapp.com/projects/%s/tickets.xml" % (
      reqdata['project'],
      reqdata['project_id'])
    ticket = xml.etree.ElementTree.Element("ticket")
    if reqdata.has_key('assigned_user_id') and reqdata['assigned_user_id']:
      subel = xml.etree.ElementTree.SubElement(ticket, "assigned-user-id")
      subel.text = reqdata['assigned_user_id']
    if reqdata.has_key('body') and reqdata['body']:
      subel = xml.etree.ElementTree.SubElement(ticket, "body")
      subel.text = reqdata['body']      
    if reqdata.has_key('state') and reqdata['state']:
      subel = xml.etree.ElementTree.SubElement(ticket, "state")
      subel.text = reqdata['state']
    if reqdata.has_key('title') and reqdata['title']:
      subel = xml.etree.ElementTree.SubElement(ticket, "title")
      subel.text = reqdata['title']      
    # serialize the xml data to a string
    data = xml.etree.ElementTree.tostring(ticket)
    response = self._submit_request(url, reqdata['token'], data)
    print 'debuggery: reading response file object'
    data_dict = self._parse_xml(response.read())
    print data_dict
    self.get_result().add_msg('ticket created !')
    return self.get_result()


  def _submit_request(self, uri, token, data, method='POST'):
    """
    Create the http request and submit it
    """
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password('Web Password', uri, token, 'x')
    auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    print 'debuggery: uri='+uri
    print 'debuggery: data='+data
    headers = { 
      'Content-Type' : 'application/xml',
      'X-LighthouseToken' : token,
      }
    req = urllib2.Request(uri, data, headers)

    if method == 'PUT':
      req.get_method = lambda: 'PUT'

    print 'debuggery: created http request object. ... opening ...'
    try:
      f = urllib2.urlopen(req)
      print 'debuggery: opened!'
      return f
    except urllib2.URLError as (exc):
      raise BleepServiceError(exc)


  def _parse_xml(self, xml_data):
    """
    Parse the xml into a python dictionary
    """
    parser = XMLParser()
    tree = parser.feed(xml_data)
    root = parser.close()
    data_dict = XmlDictConfig(root)
    return data_dict

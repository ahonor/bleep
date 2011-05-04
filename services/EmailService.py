import os
import smtplib
import email

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import ConfigParser
from django.template import Template, Context, loader

from bleeps.models import Bleep
from services.BleepService import BleepService, BleepServiceError, BleepServiceResult


__all__ = ['EmailService',]

class EmailService(BleepService):
  """
  Gateway to SMTP email service

  """

  @classmethod
  def get_service_type(cls):
    return 'email'

  PARAMS = {
    'email_from':{'desc':'the email sender'},
    'email_recipients':{'desc':'the email recipients'},
    'email_template_text':{'desc':'template path or URL to the text message template','default':'email/email.txt'},
    'email_template_html':{'desc':'template path or URL to the html message template','default':'email/email.html'},
    }
  

  def perform(self, reqdata):
    print 'debuggery: listing items in reqdata...'
    for k,v in reqdata.iteritems():
      print 'debuggery: reqdata: '+k+"="+str(v)

    # Verify required items in reqdata exists
    for keyname in ['email_from','email_recipients']: 
      if not keyname in reqdata:
        raise ValueError("missing item from reqdata: %s " % keyname)
    
    # Get the parent directory for this source file. 
    #  Needed for the template location.
    parent_dir = os.path.join(os.path.dirname(__file__), "..")

    reqdata['site_url'] = BleepService.get_site_url()
    # Compose the email message
    msg = MIMEMultipart('related')
    msg['Subject'] = "{0}".format(
      reqdata['bleep_message'] if 'bleep_message' in reqdata else 'no subject')
    msg['From']    = reqdata['email_from'] 
    msg['To']        = reqdata['email_recipients']
    msg.preamble = 'This is a multi-part message in MIME format.'
    msgAlt = MIMEMultipart('alternative')
    msg.attach(msgAlt)

    # Create the alternative text format
    # retrieve the text template
    template_name = reqdata['email_template_text'] if reqdata.has_key('email_template_text') else 'email/email.txt'
    text_template = self.__load_template(template_name)
    text = self.__expand_message_content(reqdata, text_template)
    part1 = MIMEText(text, 'text')
    msgAlt.attach(part1)
    # Create the alternative html format (preferred)
    template_name = reqdata['email_template_html'] if reqdata.has_key('email_template_html') else 'email/email.html'
    html_template = self.__load_template(template_name)
    html = self.__expand_message_content(reqdata, html_template)
    part2 = MIMEText(html, 'html')
    msgAlt.attach(part2)
    # Read the image data and define the image's ID
    msgImage = self.__logo_attachment(parent_dir)
    msg.attach(msgImage)
    try:
      smtp = self.__connect(parent_dir)
      # Send the email !
      print 'debuggery: sending the email message'
      smtp.sendmail(reqdata['email_from'], 
                    reqdata['email_recipients'], msg.as_string())
      smtp.quit()
    except smtplib.SMTPException as (err):
      raise BleepServiceError("Unable to send email. " + err.message)
    except Exception as (exc):
      raise BleepServiceError("Unexpected SMTP error. " + str(exc))
    self.get_result().add_msg('Succesfully sent email to ' + reqdata['email_recipients'])
    return self.get_result()



  def __connect(self, parent_dir):
    """
    Return an SMTP connection

    """
    # read the email configuration
    config = ConfigParser.ConfigParser(); 
    try:
      conf_file =os.path.join(parent_dir,"conf","smtp.ini") 
      print 'debuggery: reading conf_file: '+conf_file
      config.read(conf_file)
    except ConfigParser.Error as (cnferr):
      raise BleepServiceError("Failed reading config file. "+str(cnferr))
    print 'debuggery: config file parsed ok'

    smtp_server = config.get("server","host") if config.has_option("server","host") else 'localhost'
    smtp_port   = config.get("server","port") if config.has_option("server","port") else '25'

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    print 'debuggery: configured smtp server and port.'
    if config.has_option("server","tls") and config.get("server","tls").lower() == 'true':
      print 'debuggery: configuring TLS...'
      smtp.ehlo()
      smtp.starttls()
      smtp.ehlo()
    print 'configuring user/pass ...'
    # if user/password, configure it
    if config.has_option("login","username") and config.has_option("login","password"):
      smtp.login(config.get("login","username"), config.get("login","password"))
    #
    # Return the SMTP connection
    #
    return smtp


  def __expand_message_content(self, reqdata, template):
    """
    Read the given file and subsitute tokens provided in reqdata
    """
    c = Context(reqdata)
    print template.render(c)
    return template.render(c)


  def __load_template(self, name):
    template = None
    template = loader.get_template(name)
    return template


  def __logo_attachment(self, parent_dir):
    image_file = os.path.join(
        parent_dir, "assets/images","bleep-logo.png")
    try:
      fp = open(image_file,'rb'); # read as binary
    except IOError as (e):
      raise BleepServiceError(e)
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<bleepLogo.png>')
    msgImage.add_header('Filename', 'bleepLogo.png')
    return msgImage

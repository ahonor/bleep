from bleeps.models import Bleep
from services.BleepService import BleepService, BleepServiceError

__all__ = ['TrackerService',]


class TrackerService(BleepService):
  """
  A phony do nothing tracker system interface

  """
  @classmethod
  def get_service_type(cls):
    return 'tracker'

  PARAMS = {'project':{'desc':'the project name'}, }
  
  def perform(self, reqdata):
    if not reqdata.has_key('project'):
      raise BleepServiceError("mising param: project")    
    self.get_result().add_msg('doing it like a phony tracker would for the "%s" project!' % reqdata['project'])
    return self.get_result()

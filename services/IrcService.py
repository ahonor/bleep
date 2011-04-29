from services.BleepService import BleepService, BleepServiceError
import socket
import time
__all__ = ['irc',]

class IrcService(BleepService):
    """
    Post messages to an IRC channel

    """

    # IRC service params
    PARAMS = {'network':{'desc':'the irc server','default':'irc.freenode.net'},
              'port':{'desc':'the irc port','default':'6667', 'optional':True},
              'nick':{'desc':'the irc nick name'},
              'channel':{'desc': 'the channel name'},
              'message':{'desc':'the message'}
              }

    @classmethod
    def get_service_type(cls):
        return 'irc'

    def perform(self, reqdata):
        if not reqdata.has_key('channel'):
            raise BleepServiceError("mising param: channel")
        if not reqdata.has_key('message'):
            raise BleepServiceError("mising param: message")
        if not reqdata.has_key('nick'):
            raise BleepServiceError("mising param: nick")          
        network = int(reqdata['network']) if reqdata.has_key('network') else int(PARAMS['network']['default'])

        port = int(reqdata['port']) if reqdata.has_key('port') else int(PARAMS['port']['default'])
        try:
            print 'debuggery: creating socket to IRC network...'
            irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            irc.connect((network, port))
            time.sleep(2)
            print 'debuggery: connected. Sending PASS...'
            irc.send('PASS *\r\n')
            time.sleep(2)
            print 'debuggery: connected. Sending NICK...'
            irc.send('NICK %s\r\n' % reqdata['nick'] )
            print 'debuggery: connected. Sending USER...'
            irc.send('USER %s 0 * :%s\r\n' % (reqdata['nick'], reqdata['nick']))
            print 'debuggery: connected. Sending JOIN...'
            irc.send('JOIN #%s\r\n' % reqdata['channel'] )
            print 'debuggery: connected. Sending PRIVMSG...'
            irc.send('PRIVMSG #%s :%s\r\n' % (reqdata['channel'], reqdata['message']))
            print 'debuggery: connected. Sending PART...'
            irc.send('PART #%s\r\n' % reqdata['channel'] )
            print 'debuggery: connected. Sending QUIT...'
            irc.send('QUIT\r\n' )
            print 'debuggery: irc socket read: ' + self._read_socket(irc)
            irc.close()
            print 'debuggery: closed connection'
            self.get_result().add_msg('sent message: ' + reqdata['message'])
        except socket.error, msg:
            pass
        return self.get_result()


    def _read_socket(self,socket,bytecnt=4096):
        msg = ''
        done = False
        while not done:
            chunk = socket.recv(bytecnt)
            if not chunk:
                done = True
            else:
                msg = msg + chunk
        return msg

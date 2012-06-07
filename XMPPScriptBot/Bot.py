

import sleekxmpp


class BotBase():
    '''
        This is the Base class for the bots, it does not specify a default client class
        so at a minimum a concrete subclass will need to specify a client class.
        This lays out the interface for implementing classes, and provides some
        basic asynchronous callback functionality
    '''

    def __init__(self, clientClass, plugins = ['xep_0030',# Service Discovery
                                               'xep_0045',# Multi-User Chat
                                               'xep_0199',# XMPP Ping
                                               ]):
        
        
        '''
        Where's my documentation?
        '''                     
                             
        self.clientClass = clientClass
        self.client = None
        self.plugins = plugins
        self.listeners = {}
        self.connected = False
    
    def _notify_listener(self, key):
        listener = self.listeners.get(key,None)
        if listener != None:
            listener()
    def _register_listener(self, key, callback):
        self.listeners[key] = callback
        
    def auth_auth(self, pid, password):
        '''
        Where's my documentation?
        '''
        raise NotImplementedError
    
    def join_muc(self, room):
        '''
        Where's my documentation?
        '''
        raise NotImplementedError
    
    def send_message(self, message, to=None):
        '''
        Where's my documentation?
        '''
        raise NotImplementedError
    
    def signout(self):
        '''
        Where's my documentation?
        '''
        raise NotImplementedError
    
    def change_status(self, status):
        '''
        Where's my documentation?
        '''
        raise NotImplementedError

class SleekXMPPBot(BotBase):
    '''
        Where's my documentation?
    '''

    def __init__(self, clientClass=sleekxmpp.ClientXMPP):
        '''
        Where's my documentation?
        '''
        BotBase.__init__(self, clientClass=sleekxmpp.ClientXMPP)
    
    def auth_auth(self, pid, password, listener):
        '''
        Where's my documentation?
        '''
        self.client = self.clientClass(pid, password, sasl_mech='PLAIN')
        self._register_listener('auth_auth', listener)
        
        #once we have been auth/authd then we can join the room
        self.client.add_event_handler("session_start", self.start)
        self.client.add_event_handler("groupchat_message", self.__groupchat_handler)
        self.client.add_event_handler("message", self.__message_handler)
    
        for plugin in self.plugins:
            self.client.register_plugin(plugin) # Service Discovery
    
        # Connect to the XMPP server and start processing XMPP stanzas.
        if self.client.connect():
            self.client.process(block=False)

    def __groupchat_handler(self,msg):
        pass
    
    def __message_handler(self,msg):
        pass
    
        
    def start(self, event):
        '''
        Where's my documentation?
        '''
        self.connected = True 
        
        self._notify_listener('auth_auth')
            
        self.client.get_roster()
        self.client.send_presence()
        
    def join_muc(self, room, nick):
        '''
        Where's my documentation?
        '''
        if not self.connected:
            raise RuntimeError('You need to be connected before you try to join a multi user chat session')
        
        if not 'xep_0045' in self.client.plugin:
            self.client.register_plugin('xep_0045')
        
        self.client.plugin['xep_0045'].joinMUC(room,
                                        nick,
                                        wait=True)
        
    
    def send_message(self, message, to, is_group_message=False):
        '''
        Where's my documentation?
        '''
        if not self.connected:
            raise RuntimeError('You need to be connected before you attempt to send a message')
        
        if is_group_message:
            mtype='groupchat'
        else:
            mtype='message'
            
        self.client.send_message(mto=to,mbody=message,mtype=mtype)
        
    
    def signout(self):
        '''
        Where's my documentation?
        '''
        self.client.disconnect()
    
    def change_presence(self, status):
        '''
        Where's my documentation?
        '''
        if not self.connected:
            raise RuntimeError('You need to be connected before you attempt to change your presence')
        
        
        self.client.send_presence()


"""
This is the ScriptedConversationBot module, and it contains the required classes to use the XMPP protocol to
create scripted conversations using the XMPP protocol. This module doesn't know how to speak XMPP per-se it requires
you to provide a XMPP CLient class, it defaults to using SleekXMPP if you do not specify your own class.


"""


from threading import Timer
import yaml
import sleekxmpp
import logging

class BotBase():
    """
        Document Me!!
    """

    def __init__(self, clientClass, plugins = ['xep_0030',# Service Discovery
                                               'xep_0045',# Multi-User Chat
                                               'xep_0199',# XMPP Ping
                                               ], messageReceivedHandler=None):
        
        
        """Document Me

        :param clientClass: The XMPP client class to be used
        :type name: Class.
        :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                               'xep_0045',# Multi-User Chat
                                               'xep_0199',# XMPP Ping
                                               ]):
        :type state: list.
    

        
        
        """                    
                             
        self.clientClass = clientClass
        self.client = None
        self.plugins = plugins
        self.listeners = {}
        self.connected = False
        self.messageReceivedHandler = messageReceivedHandler
    
    def _notify_listener(self, key):
        listener = self.listeners.get(key,None)
        if listener != None:
            listener()
    def _register_listener(self, key, callback):
        self.listeners[key] = callback
        
    def auth_auth(self, pid, password):
        
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        raise NotImplementedError
    
    def join_muc(self, room):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        raise NotImplementedError
    
    def send_message(self, message, to=None):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        raise NotImplementedError
    
    def signout(self):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        raise NotImplementedError
    
    def change_status(self, status):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        raise NotImplementedError

class SleekXMPPBot(BotBase):

    def __init__(self, clientClass=sleekxmpp.ClientXMPP, messageReceivedHandler=None):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        BotBase.__init__(self, clientClass=sleekxmpp.ClientXMPP,messageReceivedHandler=messageReceivedHandler)
    
    def auth_auth(self, pid, password, listener):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
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
        if self.messageReceivedHandler:
            self.messageReceivedHandler(msg)
    
    def __message_handler(self,msg):
        pass
    
        
    def start(self, event):
        
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        self.connected = True 
        
        self._notify_listener('auth_auth')
            
        self.client.get_roster()
        self.client.send_presence()
        
    def join_muc(self, room, nick):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        if not self.connected:
            raise RuntimeError('You need to be connected before you try to join a multi user chat session')
        
        if not 'xep_0045' in self.client.plugin:
            self.client.register_plugin('xep_0045')
        
        self.client.plugin['xep_0045'].joinMUC(room,
                                        nick,
                                        wait=True)
        
    
    def send_message(self, message, to, is_group_message=False):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        if not self.connected:
            raise RuntimeError('You need to be connected before you attempt to send a message')
        
        if is_group_message:
            mtype='groupchat'
        else:
            mtype='message'
            
        self.client.send_message(mto=to,mbody=message,mtype=mtype)
        
    
    def signout(self):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        self.client.disconnect()
    
    def change_presence(self, status):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        if not self.connected:
            raise RuntimeError('You need to be connected before you attempt to change your presence')
        
        
        self.client.send_presence()



class Script:
    '''
        Where's my documentation?
    '''
    
    def __init__(self, **kwargs):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        if('file' in kwargs):
            
            try:
                with open(kwargs.get('file'), 'r') as script_file:
                    script_dict = yaml.load(script_file)
                    
                self.actors = script_dict['actors']
                self.script = script_dict['script']
            except IOError:
                logging.error('The script file could not be found')
                exit(-1)
            except yaml.parser.ParserError:
                logging.error('The script was not properly formed (make sure you use 4 spaces and not a tab)')
                exit(-1)
            except KeyError:
                logging.error('The script was not properly formed, you are missing one of the actors or script nodes')
                exit(-1)
        elif 'actors' in kwargs and 'script' in kwargs:
            self.actors = kwargs.get('actors')
            self.script = kwargs.get('script')
        else:
            raise AttributeError('You must specify either a yaml formatted config file, or the actors and script attributes.')   
        
        self.actorBots = {}
        
       
        self.monitorCallback = kwargs.get('monitorCallback', None)
        self.playFinishedCallback = kwargs.get('playFinishedCallback', None)
        self.running=False
    def __actor_joins(self, actor):
        
        if self.running:
            actor_config = self.actors[actor]
            callback = None
            
            if actor_config.get('monitor', None):
                callback = self.monitorCallback
                
            bot = SleekXMPPBot(messageReceivedHandler=callback)
            bot.auth_auth(actor_config['jid'], 
                          actor_config['pass'], 
                          lambda :bot.join_muc('hgg@conference.localhost', actor_config['nick']))
            
            self.actorBots[actor] = bot
    
    def __actor_leaves(self, actor):
        self.actorBots[actor].signout()
    
    def abort(self):
        self.running = False
        
        for actor in self.actorBots:
            self.__actor_leaves(actor)
            
        self.playFinishedCallback()
        
          
    def start_conversation(self):
        """
        
            Document me!
            
            :param clientClass: The XMPP client class to be used
            :type name: Class.
            :param plugins: A list of plugins to be loaded (defaults to ['xep_0030',# Service Discovery
                                                   'xep_0045',# Multi-User Chat
                                                   'xep_0199',# XMPP Ping
                                                   ]):
            :type state: list.
            :returns:  int -- the return code.
            :raises: AttributeError, KeyError
        """
        self.running = True
        self.__play_line()
        
    
    
    def __play_line(self):
        
        if self.running:
            script_line = self.script.pop(0)
            if script_line['type'] == 'JOIN':
                self.__actor_joins(script_line['actor'])
            elif script_line['type'] == 'LEAVE':
                self.__actor_leaves(script_line['actor'])
            elif script_line['type'] == 'SPEAK':
                
                actor = self.actorBots[script_line['actor']]
                actor.send_message(message=script_line['line'],
                                    to='hgg@conference.localhost', 
                                    is_group_message=True)
            if len(self.script) > 0:
                
                if script_line['delay'] > 0:
                    t = Timer(script_line['delay'], self.__play_line)
                    t.start()
                else:
                    self.__play_line()
            else:
                if self.playFinishedCallback:
                    self.playFinishedCallback()
    
    
    




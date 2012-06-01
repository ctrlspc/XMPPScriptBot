

import sys
import logging
from optparse import OptionParser
from threading import Timer
import sleekxmpp


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

class ScriptedGroupConversationBot(sleekxmpp.ClientXMPP):

    """
        A SleekXMPP bot that knows how to signin to the server, and join a predefined room.
        Can then be used be a controller object to send messages.
        Optionally you can supply a message_handler funtion which will be called everytime the bot
        detects that a message has been received in the room. 
    """

    def __init__(self, jid, password, room, nick,message_handler=None):
        """
        
        Arguments:
            jid -- the username for the jabber service eg bot1@localhost
            password -- the password to authenticate the jid
            room -- the room to join upon succesfull authorization
            nick -- the nickname to use on entering the room
            message_handler -- an optional message handler, the bot will forward any messages received to this function
            otherwise it can just be used to send messages.
        
        """
        
        sleekxmpp.ClientXMPP.__init__(self, jid, password, sasl_mech='PLAIN')#there is a bug 
        self.in_room = False
        self.room = room
        self.nick = nick

        #once we have been auth/authd then we can join the room
        self.add_event_handler("session_start", self.start)

        if message_handler is not None:
            #pass any messages received in the room off to the message handler
            self.add_event_handler("groupchat_message", message_handler)
            self.add_event_handler("message", message_handler)
    
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping
    
        # Connect to the XMPP server and start processing XMPP stanzas.
        if self.connect():
            self.process(block=False)

    def start(self, event):
        """
        Process the session_start event.

        Autjorization has been handled, so join the room

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        wait=True)
        self.in_room = True # so that the contoller can know that you are in the room.


class Script():
    
    def __init__(self):
        self.actors = {'S':{'nick':'Slartibartfast', 'jid':'bot1@localhost', 'pass':'password'},
                       'AD':{'nick':'Arthur Dent', 'jid':'bot2@localhost', 'pass':'password'},
                       'BP':{'nick':'Bowl of Petunias', 'jid':'bot3@localhost', 'pass':'password'}}
        
        self.script = [
                           {'type':'JOIN', 'actor':'S', 'delay':2},
                           {'type':'JOIN', 'actor':'AD', 'delay':2},
                           
                           {'type':'SPEAK','actor':'S', 'line':"You must come with me." , 'delay':3},
                           {'type':'SPEAK','actor':'AD', 'line':"Who are you?" , 'delay':3},
                           {'type':'SPEAK','actor':'S', 'line':"What? No. My name's not important. You must come with me, or you'll be late." , 'delay':3},
                           {'type':'SPEAK','actor':'AD', 'line':"Late for what?" , 'delay':3},
                           {'type':'SPEAK','actor':'S', 'line':"Well, um, what's your name Earthman?" , 'delay':3},
                           {'type':'SPEAK','actor':'AD', 'line':"Dent. Arthur Dent." , 'delay':3},
                           {'type':'SPEAK','actor':'S', 'line':"Well, late as in *the late* Dentarthurdent. It's a sort of threat. You see?" , 'delay':3},
                           {'type':'SPEAK','actor':'AD', 'line':"No. " , 'delay':3},
                           {'type':'SPEAK','actor':'S', 'line':"Your friends are safe, you can trust me." , 'delay':3},
                           {'type':'SPEAK','actor':'AD', 'line':"Trust a man who won't even tell me his name? " , 'delay':3},
                           {'type':'SPEAK','actor':'S', 'line':"Well, um, my name is, um, it's" , 'delay':3},
                           {'type':'SPEAK','actor':'S', 'line':"Slartibartfast. " , 'delay':3},
                           {'type':'SPEAK','actor':'AD', 'line':"What?" , 'delay':3},
                           {'type':'SPEAK','actor':'S', 'line':"I *said* it wasn't important." , 'delay':3},
                           {'type':'JOIN', 'actor':'BP', 'delay':5},
                           {'type':'SPEAK','actor':'BP', 'line':"Oh no! Not again! (SMASH)" , 'delay':1},
                           {'type':'LEAVE', 'actor':'BP', 'delay':5},
                           {'type':'LEAVE', 'actor':'S', 'delay':0},
                           {'type':'LEAVE', 'actor':'AD', 'delay':0},
                           
                       ]
        
        self.actorBots = {}
        
    def handle_message(self,msg):
        print 'got message'
        
    def __actor_joins(self, actor):
        
        actor_config = self.actors[actor]
        self.actorBots[actor] = ScriptedGroupConversationBot(actor_config['jid'], 
                                                           actor_config['pass'], 
                                                           'hgg@conference.localhost', 
                                                           actor_config['nick'])
    
    def __actor_leaves(self, actor):
        self.actorBots[actor].disconnect()
        
    def start_conversation(self):
        
        self.__play_line()
        
    
    
    def __play_line(self):
        
        script_line = self.script.pop(0)
        if script_line['type'] == 'JOIN':
            self.__actor_joins(script_line['actor'])
        elif script_line['type'] == 'LEAVE':
            self.__actor_leaves(script_line['actor'])
        elif script_line['type'] == 'SPEAK':
            
            actor = self.actorBots[script_line['actor']]
            actor.send_message(mto='hgg@conference.localhost',mbody=script_line['line'],mtype='groupchat',mfrom='bot1@localhost')
        
        if len(self.script) > 0:
            
            if script_line['delay'] > 0:
                t = Timer(script_line['delay'], self.__play_line)
                t.start()
            else:
                self.__play_line()
    
    
    

def _parse_script(script):
    """
    Parses the supplied script file. This is an INI style text file and should look something like this:
    [actors]
    S:Slartibartfast:bot1@localhost:secret_password
    AD:Arthur Dent:bot2@localhost:secret_password
    
    [script]
    S: You must come with me. :3
    AD: Who are you? :3
    S: What? No. My name's not important. You must come with me, or you'll be late. :3
    AD: Late for what? :3
    S: Well, um, what's your name Earthman? :3
    AD: Dent. Arthur Dent. :3
    S: Well, late as in *the late* Dentarthurdent. It's a sort of threat. You see? :3
    AD: No. :3
    S: Your friends are safe, you can trust me. :3
    AD: Trust a man who won't even tell me his name? :3
    S: Well, um, my name is, um, it's :3
    S: Slartibartfast. :3
    AD: What? :3
    S: I *said* it wasn't important. :3
    
    """
    
    return Script()
    



def message_handler(msg):
    
    pass

if __name__ == '__main__':
    # Setup the command line arguments.
    parser = OptionParser()

    # Output verbosity options.
    parser.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    parser.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    parser.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    parser.add_option("-s", "--script", dest="script_src",
                    help="The Conversation Script")
    

    opts, args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.script_src is None:
        print "A mandatory option is missing\n"
        parser.print_help()
        exit(-1)

    script = _parse_script(opts.script_src)    
    script.start_conversation()
    



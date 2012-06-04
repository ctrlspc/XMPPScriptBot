

import sys
import logging
from optparse import OptionParser
from threading import Timer
from Bot import SleekXMPPBot
import yaml

class Script:
    
    def __init__(self, **kwargs):
        
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
        
    
    def __actor_joins(self, actor):
        
        actor_config = self.actors[actor]
        
        bot = SleekXMPPBot()
        bot.auth_auth(actor_config['jid'], 
                      actor_config['pass'], 
                      lambda :bot.join_muc('hgg@conference.localhost', actor_config['nick']))
        
        self.actorBots[actor] = bot
    
    def __actor_leaves(self, actor):
        self.actorBots[actor].signout()
        
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
            actor.send_message(message=script_line['line'],
                                to='hgg@conference.localhost', 
                                is_group_message=True)
        if len(self.script) > 0:
            
            if script_line['delay'] > 0:
                t = Timer(script_line['delay'], self.__play_line)
                t.start()
            else:
                self.__play_line()
    
    
    



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

    script = Script(file=opts.script_src)  
    script.start_conversation()
    



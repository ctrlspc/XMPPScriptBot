"""

    Megarathea Example:
    ======================
    
    This is an example of how you might use XMPPScriptBot. To run it do the following:
    
    1. Install and configure OpenFire, be sure to use localhost as the domain (If you are doing this on a Mac, once it installs nothing happens, and you don't get any furter info.....just goto System Prefs and the OpenFire control panel is in there (restart if not))
    2. create 3 bots (bot 1, bot2, bot3 all with password "password"
    3. Install and run an XMPP client, I have used both pidgin and Openfire's companion Spark
    4. login to your client using the admin account you setup in 1.
    5. create a chat room called hgg (hgg@conference.localhost)
    6. python ScriptedConversationBot -s script.txt (the script file doesn't need to exist yet, but it will complain if you dont specify the arg (next on my todo list to implement the script parsing)
    7. sit back and watch the chat unfold in your chatroom window.

    Ps. For those in the dark about the script....http://en.wikipedia.org/wiki/Slartibartfast

"""

import csv
import logging
from optparse import OptionParser
from XMPPScriptBot.ScriptedConversationBot import Script
from datetime import datetime

start = None
dataLog = []

def parseFromField(field):
    if field:
        
        fieldComponents = field.__str__().split('/')
        
        if len(fieldComponents) == 2:
            if fieldComponents[1] == 'admin':
                return (1, fieldComponents[1])
            else:
                return (0, fieldComponents[1])
        
    return (-1, 'system')

def parseMessageField(field):
    
    if field == 'Be Nice to one antother!!':
        return 1
    elif field == 'This a warning, please stop any abusive behavior or the chat will be terminated':
        return 2
    elif field == 'This chat session will now be terminated':
        return 3
    else:
        return -1
    return 0

def monitorCallbackFuntion(msg):
    
    actor_type, actor = parseFromField(msg['from'])
    dataLog.append({'timestamp':(datetime.now() - start).total_seconds() *1000,
                    'actor':actor,
                    'message':msg['body'],
                    'actor_type':actor_type,
                    'message_type':parseMessageField(msg['body']),
                    })
    
    
def playFinishedCallback():
    #print out the dataLog to csv file
    
    with open('data.csv', 'wb') as f:
        keys = ['timestamp','actor','message','actor_type','message_type']
        dictWriter = csv.DictWriter(f,keys)
        dictWriter.writer.writerow(keys)
        dictWriter.writerows(dataLog)
    print 'done'
    
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

    opts, args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')


    script = Script(file='hgg.yaml', 
                    monitorCallback=monitorCallbackFuntion, 
                    playFinishedCallback=playFinishedCallback)  
    
    
    start = datetime.now()
    script.start_conversation()
    




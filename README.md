XMPPScriptBot
=============

Use this to create your own automated screenplays over IM

This was developed for a Psychology experiment involving user intervention to 
cyber-bullying, carried out in the School of Psychology at the University of Kent.

This project was made possible largely due to the existence of OpenFire (http://www.igniterealtime.org/projects/openfire/)
and the SleekXMPP library developed by Nathan Fritz https://github.com/fritzy/SleekXMPP

This is definitely a work in progress and I will endeavour to get it packaged properly soon.
However if you want to try it out:

1. Install and configure OpenFire, be sure to use localhost as the domain (If you are doing this on a Mac, once it installs nothing happens, and you don't get any furter info.....just goto System Prefs and the OpenFire control panel is in there (restart if not))
2. create 3 bots (bot 1, bot2, bot3 all with password "password"
3. Install and run an XMPP client, I have used both pidgin and Openfire's companion Spark
4. login to your client using the admin account you setup in 1.
5. create a chat room called hgg (hgg@conference.localhost)
6. python ScriptedConversationBot -s script.txt (the script file doesn't need to exist yet, but it will complain if you dont specify the arg (next on my todo list to implement the script parsing)
7. sit back and watch the chat unfold in your chatroom window.

Development TODO's:

1. Implement the script parser - DONE
2. Abstract the dependency on SleekXMPP (so that you can use whatever xmpp library you like, and for easier unittests)
3. Proper Sphinx docs

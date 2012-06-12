import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "XMPPScriptBot",
    version = "0.0.1",
    author = "Jason Marshall",
    author_email = "ctrlspc@gmail.com",
    description = ("A utility for creating scripted 'plays' to be delivered over Instant Messenger via the XMPP protocol"),
    license = "MIT",
    keywords = "XMPP IM script",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['XMPPScriptBot',],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['sleekxmpp']
)

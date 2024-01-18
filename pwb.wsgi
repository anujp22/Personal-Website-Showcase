#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/pwb/")

from pwb import app as application
application.secret_key = 'Adding-secretkey-1022'


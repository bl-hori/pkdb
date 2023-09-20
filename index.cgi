#!/home/blrecruit/broadleaf.co.jp/public_html/lab/pkdb/.venv/bin/python

import os

from wsgiref.handlers import CGIHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.base')

application = get_wsgi_application()
CGIHandler().run(application)

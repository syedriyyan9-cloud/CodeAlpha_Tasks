# """
# WSGI config for event_registration_system project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration_system.settings')

# application = get_wsgi_application()

# your_project_name/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

application = get_wsgi_application()
app = application  # <-- ADD THIS LINE FOR VERCEL
from models import SiteUser
import os
from os import listdir
from django.contrib.auth.models import User

def handle_uploaded_file(f, title, user):
  targetdir = 'uploads/' + user.__str__() + '/incoming/'
  if not os.path.exists(targetdir):
    os.makedirs(targetdir)
  with open(targetdir + title, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)


def user_is_admin(user):
  return user.is_superuser

def is_admin(request):
  return request.user.is_superuser

def list_files(account, mode):
  targetdir = 'uploads/' + account.__str__() + mode
  if os.path.exists(targetdir):
    return [ f for f in listdir(targetdir) ]
  else:
    return False


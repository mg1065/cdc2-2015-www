import os
from os import listdir
from django.conf import settings


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
    targetdir = os.path.join('uploads', account.username, mode)
    if os.path.exists(targetdir):
        return [f for f in listdir(targetdir)]
    else:
        return False


def create_user_uploads(user):
    userdir = os.path.join(settings.MEDIA_ROOT, user.username)
    if not os.path.exists(userdir):
        incoming = os.path.join(userdir, 'incoming')
        outgoing = os.path.join(userdir, 'outgoing')

        # TODO: Fix perms?
        os.makedirs(incoming)
        os.chmod(incoming, 0777)
        os.makedirs(outgoing)
        os.chmod(outgoing, 0777)
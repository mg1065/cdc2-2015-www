from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from models import SiteUser, Testimonial
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .actions import *

def index(request):
  if request.GET.get('logout', False):
    context = { 'script' : 'True' }
    return render(request, 'cdc/index.html', context)
  return render(request, 'cdc/index.html')

def contact(request):
  return render(request, 'cdc/contact.html')

def about(request):
  return render(request, 'cdc/about.html')


# Testimonial
def testimonials(request):
  user = None
  if request.user.is_authenticated():
    user = get_user(request)
  return render(request, 'cdc/testimonials.html', { 'testimonials' : Testimonial.objects.all(), 'user' : user })


@login_required
def testimonials_delete(request, t_id):
  entry = get_object_or_404(Testimonial, pk=t_id)
  entry.delete()
  return redirect(reverse('cdc:testimonials'))

def form(request):
  form = TestimonialForm(request.POST)
  if form.is_valid():
      form.save()
      return redirect(reverse('cdc:testimonials'))
  return render_to_response('cdc/form.html', {'form': form})


def login_view(request):
  if request.user.is_authenticated():
    return redirect('cdc:index')

  username = request.POST.get('account', None)
  company = request.POST.get('company', None)
  pin = request.POST.get('pin', None)

  user = authenticate(username=username, password=pin)
  if user is not None:
    if user.is_active:
      if user.site_user.company == company:
        login(request, user)
        return redirect('cdc:index')
      else:
        context = {'error': "Please fill out all fields before submitting."}
    else:
      context = {'error': "The user you requested was not found." }
  else:
    context = {}
  return render(request, 'cdc/login.html', context)


def login_admin(request):
  if request.user.is_authenticated():
    return redirect('cdc:index')

  username = request.POST.get('username', None)
  password = request.POST.get('password', None)

  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      login(request, user)
      return redirect('cdc:admin')
  return render(request, 'cdc/admin.html')


def settings(request):
  return render(request, 'cdc/settings.html')


@login_required
def logout_view(request):
  logout(request)
  return redirect(reverse('cdc:index'))

@login_required
def account_home(request):
  user = get_user(request)
  page = request.GET.get('page', False)
  success = request.GET.get('success', False)
  context = { 'user' : user, 'page' : page }
  return render(request, 'cdc/account.html', context)

@login_required
def upload(request):
  user = get_user(request).username
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      handle_uploaded_file(request.FILES['file'], request.POST['title'], user)
      return HttpResponseRedirect('success')
  else:
    form = UploadFileForm()
  return render_to_response('cdc/upload.html', {'form': form})


def success(request):
  return render(request, 'cdc/success.html')

@login_required
def filings(request):
  user = get_user(request)
  files = list_files(user, '/incoming/')
  return render(request, 'cdc/files.html', { 'files' : files, 'user' : user, 'mode' : 'incoming' })

@login_required
def reports(request):
  user = get_user(request)
  files = list_files(user, '/outgoing/')
  return render(request, 'cdc/files.html', { 'files' : files, 'user' : user, 'mode' : 'outgoing' })

def admin(request):
  message = ''
  files = None
  create = None
  accounts = None
  if request.GET.get('user_button', False):
    create = 'newuser'
  elif request.GET.get('admin_button', False):
    create = 'newadmin'
  # Password reset
  if request.POST.get('pwreset', False):
    user = get_object_or_404(User, username=request.POST['account'])
    user.set_password(request.POST.get('pin', False))
    user.save()
    message += 'Password successfully reset!\n'
  # Delete User
  if request.POST.get('delete', False):
    user = get_object_or_404(User, username=request.POST['account'])
    user.delete()
    message += 'User successfully deleted!\n'
  # Create new site user
  if request.POST.get('newuser', False):
    if User.objects.filter(username=request.POST.get('account', False)).exists():
      message += 'Error: User already exists in database.\n'
    else:
      user = User.objects.create_user(request.POST.get('account', False), '', request.POST.get('pin', False))
      siteuser = SiteUser(user=user, company=request.POST.get('company', False))
      siteuser.save()
      # Create the upload and download directories for the new user
      targetdir = 'uploads/' + user.username
      if not os.path.exists(targetdir):
        os.makedirs(targetdir + '/incoming')
        os.chmod(targetdir + '/incoming', 0777)
        os.makedirs(targetdir + '/outgoing')
        os.chmod(targetdir + '/outgoing', 0777)
      message += 'User successfully created!\n'
  # Create new admin
  if request.POST.get('newadmin', False):
    if User.objects.filter(username=request.POST.get('account', False)).exists():
      message += 'Error: User already exists in database.\n'
    else:
      user = User.objects.create_user(request.POST.get('username', False), '', request.POST.get('password', False))
      user.is_superuser = True
      user.save()
      siteuser = SiteUser(user=user, company="Admin")
      siteuser.save()
      message += 'Admin successfully created!\n'
  # Delete a file
  if request.GET.get('delete', False):
    try:
      os.remove(request.GET['delete'])
      message += 'File \'' + request.GET['delete'] + '\' deleted!\n'
    except OSError:
      message += 'That file does not exist.\n'
  # List a user's files
  if request.GET.get('search', False):
    files = list_files(request.GET.get('search', ''), '/' + request.GET.get('mode', ''))
    if not files:
      message += "No files found!\n"
  if request.GET.get('list_users', False):
    accounts = User.objects.all()
  if get_user(request) and get_user(request).is_superuser:
    return render(request, 'cdc/account.html', { 'users' : accounts, 'create' : create, 'message' : message, 'files' : files, 'mode' : request.GET.get('mode', False), 'search' : request.GET.get('search', False), 'user' : get_user(request) })
  return HttpResponseRedirect('login/admin')

from django.shortcuts import render ,render_to_response , get_object_or_404 , reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse ,HttpResponseRedirect
from django.views import View
from .forms import UserLoginForm, UserRegisterForm,UserLoginFormcaptcha
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
    )
from django.db.models import Q

@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class error_superuser(View):
    def get(self, request):
        return render(request, "error_superuser.html")

#@method_decorator(user_passes_test(lambda u: u.is_superuser,loggiin_url='/sign/dashboard/error_superuser'), name='dispatch')
class users_list(View):
    def get(self, request):
        groups = Group.objects.all()
        for obj in groups:
            print(obj)
        context = {
            'query_results': User.objects.all(),
            'groups':groups
        }
        return render(request, "users_list.html",context)

@method_decorator(user_passes_test(lambda u: u.is_superuser,login_url='/sign/dashboard/error_superuser'), name='dispatch')
class user_list_request_select_item(View):
    def post (self, request, *args, **kwargs):
        if (self.request.POST['submitbutton']=='حذف کاربر'):
            del_items = request.POST.getlist('checks')
            for d in del_items:
                user = User.objects.get(id=d)
                if user.is_superuser:
                    print("شما در حال حذف مدیر هستید!!!")
                else:
                    User.objects.filter(pk=d).delete()
            return redirect(reverse('app1:users_list'))
        return redirect(reverse('app1:users_list'))
@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class user_info(View):
    def get(self, request):
        return render(request, "user_info.html")

@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class user_info_edit(View):
    def get(self, request):
        return render(request, "user_info_edit.html")

@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class dashboard(View):
    def get (self, request):
        return render(request, "index.html", {})

class Log_in(View):
    form = []
    test_form = 0
    template_name = 'login.html'
    context = {
        'message_error': ''
    }

    def get(self, request):
        self.form = UserLoginForm()
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        x = User.objects.all()
        print(x)
        if 'captcha_1' in request.POST:
            if not UserLoginFormcaptcha(request.POST).is_valid():
                self.context = {
                    'message_error': 'اطلاعات وارد شده صحیح نمیباشد',
                    'form': UserLoginFormcaptcha,
                }
                return render(request, "login.html", self.context)
        user = authenticate(username=username, password=password)
        self.context = {
            'message_error': ''
        }
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/sign/dashboard')
            else:
                self.context = {
                    'message_error': 'حساب کابری فعال نمیباشد'
                }
                return render(request, "login.html", self.context)
        else:
            print("go to log_captcha")
            self.form = UserLoginFormcaptcha
            self.test_form = 1
            self.context = {
                'message_error': 'اطلاعات وارد شده صحیح نمیباشد',
                'form':self.form
            }
            return render(request, "login.html",self.context)

@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class Log_out(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/sign/dashboard')

@method_decorator(user_passes_test(lambda u: u.is_superuser,login_url='/sign/dashboard/error_superuser'), name='dispatch')
class Log_register(View):
    template_name1 = 'register.html'
    def get(self, request):
        content = { }
        content['form'] = UserRegisterForm
        return render(request, self.template_name1, content)

    def post(self, request):
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/sign/dashboard/users_list')
        else:


            context = {}
            context={
                'form':form,
                'error_message': 'اطلاعات وارد شده صحیح نمیباشد'
            }
            return render(request, self.template_name1, context)

@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class change_password(View):
    template_name = 'change_password.html'
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect('/sign/logout')
        else:
            messages.error(request, 'Please correct the error below.')

from .forms import Edit_user_form
from django.views.generic.edit import UpdateView
@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class Edit_user_view(UpdateView):
    def get(self, request):
        user = request.user
        form = Edit_user_form(request.POST,initial= {'first_name': user.first_name , 'last_name':user.last_name , 'email' :user.email})
        return render(request, 'user_info_edit.html', {'form': form})
    def post(self, request):
        form = Edit_user_form(request.POST or None)
        if form.is_valid():
            user = request.user
            user.username = request.user.username
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            return HttpResponseRedirect('/sign/dashboard/user_info')
        else:
            user = request.user
            form = Edit_user_form(request.POST, initial={'first_name': user.first_name, 'last_name': user.last_name,'email': user.email})


        return render(request,'users_list.html',{'form':form})
from django.views.generic.list import ListView
from .models import requset_pu
from django.views.generic.edit import CreateView
@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class re_saving(CreateView):
    model = requset_pu
    template_name = 'save_request.html'

    fields = ['title','ex_request','dead_line','combo_kind']

    def form_valid(self, form):
        f = form.save(commit=False)
        f.r_user = self.request.user
        f.save()
        return redirect(reverse('app1:list_letter'))

from django.views.generic.list import ListView
@method_decorator(login_required(login_url='/sign/dashboard/login'), name='dispatch')
class list_requests(ListView):
    model = requset_pu
    template_name = "list_view.html"
    context_object_name = 'obj_of_request'

    def get_queryset(self):
        list_all = requset_pu.objects.all()
        find_object = self.request.GET.get('q')
        if find_object:
            list_all = list_all.filter(
                Q(combo_kind__icontains=find_object) |
                Q(title__icontains=find_object) |
                Q(dead_line__icontains=find_object) |
                Q(ex_request__icontains=find_object) |
                Q(r_user__last_name__icontains=find_object) |
                Q(r_user__first_name__icontains=find_object) |
                Q(dead_line__icontains=find_object)
            )
        return list_all


@method_decorator(user_passes_test( lambda u:u.is_superuser,login_url='/sign/dashboard/error_superuser' ), name='dispatch')
class delete_request(View):
  def post(self, request, *args, **kwargs):
      if self.request.POST['deletebutton']=='حذف درخواست':
          del_items = request.POST.getlist('checks')
          for d in del_items:
             del_items = requset_pu.objects.filter(id=d)
             if del_items:
                 del_items.delete()
          return redirect(reverse('app1:list_letter'))
      return redirect(reverse('app1:list_letter'))




class updates(UpdateView):
    template_name = "update_view.html"
    model = requset_pu
    context_object_name = 'obj_of_update'
    fields = [
    'combo_kind',
    'title',
    'ex_request',
    'dead_line',
   'title'
    ]

























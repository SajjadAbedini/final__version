
from django.urls import path , include
from .views import  updates,list_requests ,delete_request, user_list_request_select_item,Log_in ,re_saving,Log_out ,Log_register, dashboard,user_info,Edit_user_view,users_list,error_superuser,change_password

urlpatterns = [
    path('dashboard/login/', Log_in.as_view(), name = "login"),
    path('logout/', Log_out.as_view(), name = "logout"),
    path('register/', Log_register.as_view(), name = "register"),
    path('dashboard/', dashboard.as_view(), name = "dashboard"),
    path('dashboard/user_info', user_info.as_view(), name = "user_info"),
    path('dashboard/change_password', change_password.as_view(), name = "change_password"),
    path('dashboard/users_list', users_list.as_view(), name = "users_list"),
    path('dashboard/users_list_select', user_list_request_select_item.as_view(), name="users_list_select"),
    path('dashboard/error_superuser', error_superuser.as_view(), name = "error_superuser"),
    path('dashboard/user_info/edit/', Edit_user_view.as_view(), name='edit'),
    path('dashboard/letter/',re_saving.as_view(),name = 'letter'),
    path('dashboard/letter/list',list_requests.as_view(),name = "list_letter"),
    path('dashboard/letter/delete',delete_request.as_view(),name = "delete_request"),
    path('dashboard/letter/update',updates.as_view(),name = "updating")

]
urlpatterns += [
    path('captcha/', include('captcha.urls')),
]
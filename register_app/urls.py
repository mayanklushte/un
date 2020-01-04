from django.urls import path
from register_app import views
from django.conf import settings
from django.conf.urls.static import static
from .views import GeneratePdf

app_name = 'register_app'

urlpatterns = [
    path('user/', views.users, name='u_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('doc/', views.doc_users, name='d_register'),
    path('doc_login/', views.doc_login, name='doc_login'),
    path('doc_logout/', views.doc_logout, name='doc_logout'),

    path('users/', views.doc_list, name='u_user'),
    path('users/<int:id>/', views.pat_detail, name='detail'),
    path('docters/', views.pat_list, name='u_docter'),

    path('search/', views.search, name='search'),
    path('search/<int:id>/',views.d_detail1,name='d_details'),


    path('Appointments/<int:id>/', views.p_appoint, name='p_appoint'),
    path('appoin/', views.appoint_list, name='u_appoint'),
    path('appoin/<int:id>/', views.appoint_list1, name='appoint'),
    path('acc/<id>/', views.accept, name='accept'),
    path('rej/<id>/', views.reject, name='reject'),
    path('acc_app/', views.acc_list, name='acc_app'),
    path('acc_app/<int:id>/',views.pat_info,name='pat_info'),
    path('pat_dat/<int:id>/', views.pat_detail_form_view, name='pat_dat'),
    path('acc_app_tomo/', views.acc_list_tomo, name='acc_app_tomo'),
    path('acc_app_tomo/<int:id>',views.pat_info,name='pat_info_tomo'),
    path('p_acc_list/',views.H_doc_list,name='h_doc'),
    path('p_acc_list/<int:id>/',views.pat_pat_info,name='pat_pat_info'),
    path('req_stat/', views.req_stat, name='req_stat'),
    path('female/', views.add, name='add'),
    path('female/thanks/', views.thanks, name='thanks'),
    path('male/', views.M_input, name='M_add'),
    path('male/M_thanks/', views.M_thanks, name='M_thanks'),
    path('BMI/', views.BMI, name='BMI'),
    path('BMI/BMI_O/', views.BMI_O, name='BMI_O'),
    path('TBW/', views.TBW, name='TBW'),
    path('TBW/TBW_O/', views.TBW_O, name='TBW_O'),
    path('TBW_F/', views.TBW_F, name='TBW_F'),
    path('TBW_F/TBW_OF/', views.TBW_OF, name='TBW_OF'),
    path('rp/<int:id>/', views.report_view, name='report'),
    path('vrp/<int:id>/',views.pat_report_view,name='p_report'),
    path('pdf/<int:id>/', GeneratePdf.as_view()),
    path('appoint/', views.appoint_list2, name='pl_appoint'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

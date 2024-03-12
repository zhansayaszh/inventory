from django.urls import path
from . import views


urlpatterns = [
    #Index page
    path('',views.homepage,name=''),
    
    #Accounts
#     path('register/',views.my_register,name='my_register'),
    path('login/',views.my_login,name='my_login'),
    path('dashboard/',views.my_dashboard,name='my_dashboard'),
    path('logout/',views.my_logout,name='my_logout'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    #Forget Password
    path('password_reset_done/', views.my_password_reset_done, name='my_password_reset_done'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', views.MyUserPasswordResetConfirmView.as_view(),
         name="my_password_reset_confirm"),
    path('accounts/password_reset_complete/', views.MyUserPasswordResetCompleteView.as_view(),
         name='my_password_reset_complete'),
    
    #Companies
    path('staff/companies/', views.company_list, name='company_list'),
    path('staff/companies/create/', views.company_create, name='company_create'),
    path('staff/companies/<int:pk>/update/', views.company_update, name='company_update'),
    path('staff/companies/<int:pk>/delete/', views.company_delete, name='company_delete'),
    
    # Role URLs
    path('staff/roles/', views.role_list, name='role_list'),
    path('staff/roles/create/', views.role_create, name='role_create'),
    path('staff/roles/<int:pk>/update/', views.role_update, name='role_update'),
    path('staff/roles/<int:pk>/delete/', views.role_delete, name='role_delete'),
    
    #Users
    path('staff/users/', views.user_list, name='user_list'),
    path('staff/users/create/', views.user_create, name='user_create'),
    path('staff/users/<int:pk>/update/', views.user_update, name='user_update'),
    path('staff/users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    #My profile
    path('myprofile/', views.my_profile, name='my_profile'),
    path('myprofile/<int:pk>/update/', views.user_profile_update, name='user_profile_update'),
    
    #Change Password
    path('myprofile/change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('myprofile/password-change-done/', views.CustomPasswordChangeDoneView.as_view(), name='my_password_change_done'),
    #Items
    path('staff/items/', views.item_list, name='item_list'),
    path('staff/items/create/', views.item_create, name='item_create'),
    path('staff/items/<int:pk>/update/', views.item_update, name='item_update'),
    path('staff/items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    
    #QR code
    path('staff/items/qr_result_page/<str:qr_code>', views.qr_result_page, name='qr_result'),
    path('staff/items/all_qr_ids/', views.all_qr_ids, name='all_qr_ids'),
    
    #Excel file import
    path('staff/items/import_items/', views.import_items, name='import_items'),
    
    #My item page
    path('my_item/', views.my_item_page, name='my_item_page'),
    
]

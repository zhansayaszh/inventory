from django.shortcuts import render, redirect, get_object_or_404
from . forms import CreateUserForm, LoginForm, MyUserSetPasswordForm, CustomPasswordChangeForm
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate,login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, UserChangeForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.cache import cache
from .models import UserProfile
from inventory.models import CompanyModel, RoleModel, ItemModel
from inventory.forms import CompanyModelForm,RoleModelForm, ItemModelForm, UploadFileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import locale
from django.http import JsonResponse, HttpResponseNotFound
from inventory.load_excel import agrofintech_clean, load_excel,bass_holding_clean,bass_gold_clean
import pandas as pd, numpy as np, re

def homepage(request):
    
    return render(request,'accounts/index.html')


def my_login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("my_dashboard")  # Redirect to dashboard upon successful login
            else:
                form.add_error('password', 'Incorrect password')# Add error message for incorrect password
                

    context = {'loginform': form}
    return render(request, 'accounts/my_login.html', context=context)

def my_logout(request):
    auth.logout(request)
    
    return redirect("")

def my_password_reset_done(request):
    
    return render(request,'accounts/my_password_reset_done.html')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Пароль восстановления доступа был отправлен на вашу почту.')
            return redirect('my_password_reset_done')  # Redirect to login page after sending the reset email
    else:
        form = PasswordResetForm()

    # Add crispy form helper
    helper = FormHelper()
    helper.form_method = 'post'
    form.helper = helper

    return render(request, 'accounts/forgot_password.html', {'forget_form': form})

class MyUserPasswordResetCompleteView(PasswordResetCompleteView):
  template_name = 'accounts/my_password_reset_complete.html'


class MyUserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/my_reset_password.html'
  form_class = MyUserSetPasswordForm
  success_url = reverse_lazy("my_password_reset_complete")
  
  def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user_profile = UserProfile.objects.filter(user__email=email).first()

        if user_profile:
            if user_profile.last_password_reset_email_sent_time:
                time_since_last_email = timezone.now() - user_profile.last_password_reset_email_sent_time
                if time_since_last_email.total_seconds() < 5 * 60:  # 5 minutes in seconds
                    messages.error(request, "Password reset email already sent. Please wait before requesting another one.")
                    return self.form_invalid(request, **kwargs)

            # If it's been more than 5 minutes or no email has been sent before, proceed with sending the email
            user_profile.last_password_reset_email_sent_time = timezone.now()
            user_profile.save()

        return super().post(request, *args, **kwargs)

  
@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')

@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect('my_login')
    
    return render(request, 'accounts/staff_dashboard.html')

@login_required(login_url="my_login")
def my_dashboard(request):
    if request.user.is_superuser:
        # Redirect superusers to admin page
        return redirect('admin:index')  # Redirect to Django admin index page
    elif request.user.is_staff:
        # Redirect staff/admin users to staff dashboard
        return redirect('staff_dashboard')  
    else:
        # Regular users go to user dashboard
        return render(request, "accounts/user_dashboard.html")

# Company views
def company_list(request):
    companies = CompanyModel.objects.filter(is_active=True)
    return render(request, 'inventory/company_list.html', {'companies': companies,
                                                           'user': request.user})

def company_create(request):
    if request.method == 'POST':
        form = CompanyModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyModelForm()
    return render(request, 'inventory/company_form.html', {'form': form, 'action': 'Create'})


def company_update(request, pk):
    company = get_object_or_404(CompanyModel, pk=pk)
    if request.method == 'POST':
        form = CompanyModelForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyModelForm(instance=company)
    return render(request, 'inventory/company_form.html', {'form': form, 'action': 'Update'})


def company_delete(request, pk):
    company = get_object_or_404(CompanyModel, pk=pk)
    if request.method == 'POST':
        print("Before delete:", company.is_active)
        company.delete()
        print("After delete:", company.is_active)  # This might print False
        return redirect('company_list')
    return render(request, 'inventory/company_list.html', {'companies': CompanyModel.objects.all()})

#Role views

def role_list(request):
    roles = RoleModel.objects.filter(is_active=True)
    return render(request, 'inventory/role_list.html', {'roles': roles})


def role_create(request):
    if request.method == 'POST':
        form = RoleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleModelForm()
    return render(request, 'inventory/role_form.html', {'form': form, 'action': 'Create'})


def role_update(request, pk):
    role = get_object_or_404(RoleModel, pk=pk)
    if request.method == 'POST':
        form = RoleModelForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleModelForm(instance=role)
    return render(request, 'inventory/role_form.html', {'form': form, 'action': 'Update'})


def role_delete(request, pk):
    role = get_object_or_404(RoleModel, pk=pk)
    if request.method == 'POST':
        print("Before delete:", role.is_active)
        role.delete()
        print("After delete:", role.is_active)  # This might print False
        return redirect('role_list')
    return render(request, 'inventory/role_list.html', {'roles': RoleModel.objects.all()})

#Users
def user_list(request):
    users_list = UserProfile.objects.select_related('user').filter(user__is_active=True)
    search_query = request.GET.get('q')
    company_filter = request.GET.get('company')

    # Apply search query filter
    if search_query:
        users_list = users_list.filter(Q(user__first_name__icontains=search_query) | 
                                       Q(user__last_name__icontains=search_query) | 
                                       Q(user__email__icontains=search_query))

    # Apply company filter
    if company_filter:
        users_list = users_list.filter(company_id=company_filter)

    # Sorting
    sort_by = request.GET.get('sort_by')
    sort_direction = request.GET.get('sort_direction', 'asc')
    if sort_by:
        sort_field = sort_by  # Use the field name directly
        
        if sort_direction == 'asc':
            users_list = users_list.order_by(sort_field)
        else:
            users_list = users_list.order_by('-' + sort_field)
    
    paginator = Paginator(users_list, 10)  # Show 10 users per page
    
    page_number = request.GET.get('page')
    try:
        users = paginator.page(page_number)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        
    company_list = CompanyModel.objects.filter(is_active=True)
    
    context = {
        'users': users,
        'search_query': search_query,
        'selected_company': company_filter,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'company_list': company_list,
    }
    
    return render(request, 'inventory/user_list.html', context)

def user_create(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CreateUserForm()
    return render(request, 'inventory/user_form.html', {'registerform': form, 'action': 'Create'})


def user_update(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    user_id = user_profile.user_id  # Retrieve the user_id from UserProfile

    # Now you have the user_id, you can use it to retrieve the User instance
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            # Update UserProfile instance
            user_profile.company = form.cleaned_data.get('company')
            user_profile.role = form.cleaned_data.get('role')
            user_profile.save()
            return redirect('user_list')
    else:
        form = CreateUserForm(instance=user, initial={'company': user_profile.company, 'role': user_profile.role})
    return render(request, 'inventory/user_form.html', {'registerform': form, 'action': 'Update'})

@login_required
def my_profile(request):
    user_profile = request.user.userprofile  # Assuming the UserProfile is related to the User model via a OneToOneField named 'userprofile'
    return render(request, 'inventory/my_profile.html', {'user_profile': user_profile})

@login_required
def user_profile_update(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    user_id = user_profile.user_id  # Retrieve the user_id from UserProfile

    # Now you have the user_id, you can use it to retrieve the User instance
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            # Update UserProfile instance
            user_profile.company = form.cleaned_data.get('company')
            user_profile.role = form.cleaned_data.get('role')
            user_profile.save()
            return redirect('my_profile')
    else:
        form = CreateUserForm(instance=user, initial={'company': user_profile.company, 'role': user_profile.role})
    return render(request, 'inventory/user_form_profile.html', {'registerform': form, 'action': 'Update'})


def user_delete(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    user_id = user_profile.user_id  # Retrieve the user_id from UserProfile

    user = get_object_or_404(User, pk=user_id)  # Retrieve the corresponding User instance

    if request.method == 'POST':
        print("Before delete:", user.is_active)
        user.is_active = False
        user.save()
        print("After delete:", user.is_active)
        return redirect('user_list')
    
    return render(request, 'inventory/user_list.html', {'user': user_profile})



def truncate_text(text, max_length=30, suffix='...'):
    """
    Truncates text to a specified length.
    """
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length-len(suffix)] + suffix
    
#Items
def item_list(request):
    # Set locale to Russian
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    items_list = ItemModel.objects.filter(is_active=True)
    search_query = request.GET.get('q')
    company_filter = request.GET.get('company')

    # Apply search query filter
    if search_query:
        items_list = items_list.filter(Q(name__icontains=search_query) | 
                                       Q(qr_id__icontains=search_query) |
                                       Q(item_idx__icontains=search_query))

    # Apply company filter
    if company_filter:
        items_list = items_list.filter(company_id=company_filter)

    # Sorting
    sort_by = request.GET.get('sort_by')
    sort_direction = request.GET.get('sort_direction', 'asc')
    if sort_by:
        sort_field = sort_by  # Use the field name directly
        
        if sort_direction == 'asc':
            items_list = items_list.order_by(sort_field)
        else:
            items_list = items_list.order_by('-' + sort_field)
    
    paginator = Paginator(items_list, 7)  # Show 6 items per page
    
    page_number = request.GET.get('page')
    try:
        items = paginator.page(page_number)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    company_list = CompanyModel.objects.filter(is_active=True)
    user_list = User.objects.filter(is_active=True)
    
    # Shorten long text fields
    for item in items:
        item.name = truncate_text(item.name)
        # Add more fields to truncate if needed
        
    context = {
        'items': items,
        'company_list': company_list,
        'user_list':user_list,
        'search_query': search_query,
        'selected_company': company_filter,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
    }
    
    return render(request, 'inventory/item_list.html', context)

def all_qr_ids(request):
    # Fetch all qr_ids
    qr_ids = ItemModel.objects.filter(is_active=True).values_list('qr_id', flat=True)
    
    # Convert qr_ids queryset to a list
    qr_ids_list = list(qr_ids)
    
    return JsonResponse({'qr_ids': qr_ids_list}, safe=False)

def item_create(request):
    if request.method == 'POST':
        form = ItemModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemModelForm()
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Create'})


def item_update(request, pk):
    item = get_object_or_404(ItemModel, pk=pk)
    if request.method == 'POST':
        form = ItemModelForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemModelForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Update'})




def item_delete(request, pk):
    item = get_object_or_404(ItemModel, pk=pk)
    if request.method == 'POST':
        print("Before delete:", item.is_active)
        item.delete()
        print("After delete:", item.is_active)  # This might print False
        return redirect('item_list')
    return render(request, 'inventory/item_list.html', {'item': ItemModel.objects.all()})

def import_items(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle file upload
            excel_file = request.FILES['file']
            
            # Load Excel file into DataFrame
            df = load_excel(excel_file)

            # Clean and transform data
            company = form.cleaned_data['company']
            
            cleaning_functions = {
                'agrofintech': agrofintech_clean,
                'bass holding': bass_holding_clean,
                'bass gold': bass_gold_clean
            }
            cleaning_function = cleaning_functions.get(company.name.lower())

            if cleaning_function is None:
                # Handle the case when no cleaning function is found for the company
                raise ValueError(f"No cleaning function found for company: {company.name}")
            
            df_values = cleaning_function(df)[0]
            items_data = df_values.to_dict(orient='records')
            #ItemModel.objects.bulk_create([ItemModel(**item) for item in items_data])
            for item_data in items_data:
                item_idx = item_data['item_idx']
                # Check if an item with the same ID already exists for the selected company
                existing_item = ItemModel.objects.filter(item_idx=item_idx, company=company).exists()
                
                if not existing_item:
                    # Item does not exist, proceed with insertion
                    item_data['company'] = company
                    ItemModel.objects.create(**item_data)

            return redirect('item_list')  # Redirect to a success page
    else:
        form = UploadFileForm()

    return render(request, 'inventory/import_items.html', {'form': form})

def qr_result_page(request, qr_code):
    print("QR Code:", qr_code)
    try:
        item = ItemModel.objects.get(qr_id=qr_code)
        print("Item found:", item)
        context = {'item': item}
        return render(request, 'inventory/qr_result.html', context)
    except ItemModel.DoesNotExist:
        print("Item not found")
        return HttpResponseNotFound("QR code data not found.")


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
  template_name = 'accounts/my_password_change_done.html'

   
class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('my_password_change_done')
    template_name = 'accounts/change_password.html'
    
    
    def form_valid(self, form):
        messages.success(self.request, 'Ваш новый пароль установлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибку.')
        return super().form_invalid(form)

def my_item_page(request):
    user = request.user  # Get the logged-in user
    assigned_items = ItemModel.objects.filter(user=user)  # Query items assigned to the user
    return render(request, 'inventory/my_item_page.html', {'assigned_items': assigned_items})
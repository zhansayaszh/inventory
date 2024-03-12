from django.shortcuts import render
from .models import CompanyModel, RoleModel
# Create your views here.
def company_list(request):
    companies = CompanyModel.objects.filter(is_active=True)
    return render(request, 'company_list.html', {'companies': companies})

def role_list(request):
    roles = RoleModel.objects.filter(is_active=True)
    return render(request, 'role_list.html', {'roles': roles})
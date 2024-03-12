from django.db import models
from django.contrib.auth.models import User
from inventory.models import CompanyModel, RoleModel
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(RoleModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    def is_staff_russian(self):
        return _('Да') if self.user.is_staff else _('Нет')

    is_staff_russian.short_description = _('Staff Status')
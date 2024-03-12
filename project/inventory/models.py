from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CompanyModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'companies'
    
    def delete(self, using=None, keep_parents=False):
        # Instead of deleting, set is_active to False
        self.is_active = False
        self.save()
    def __str__(self):
        return self.name
    
class RoleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'roles'
    
    def delete(self, using=None, keep_parents=False):
        # Instead of deleting, set is_active to False
        self.is_active = False
        self.save()
    def __str__(self):
        return self.name

class ItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    date = models.DateField(null=True, blank=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    residual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_idx = models.CharField(max_length=100)
    qr_id = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'items'
        
    def delete(self, using=None, keep_parents=False):
        # Instead of deleting, set is_active to False
        self.is_active = False
        self.save()
    def __str__(self):
        return self.name
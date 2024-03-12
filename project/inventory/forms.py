from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import ItemModel, CompanyModel, RoleModel
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User


# class UserModelForm(forms.ModelForm):
#     class Meta:
#         model = UserModel
#         # fields = '__all__'
#         fields= ('name','email','role','company')
#         labels={
#             'name':'ФИО',
#             'email':'Электронная почта',
#             'role':"Должность",
#             'company':'Компания'
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
        
#         self.fields['role'].empty_label='Выбрать'
#         self.fields['company'].empty_label='Выбрать' 
#          # Filter out inactive roles and companies
#         self.fields['role'].queryset = RoleModel.objects.filter(is_active=True)
#         self.fields['company'].queryset = CompanyModel.objects.filter(is_active=True)
    
#     def clean_name(self):
#         name = self.cleaned_data['name']

#         # Split the name into words
#         words = name.split()

#         # Check if there are at least two words
#         if len(words) < 2:
#             raise forms.ValidationError("Не полное ФИО")

#         # Check if each word starts with a capital letter
#         for word in words:
#             if not word.istitle():
#                 raise forms.ValidationError("ФИО должно быть с заглавной буквы")

#         return name
    
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         user_id = self.instance.id if self.instance else None

#         # Check if the email has changed
#         if UserModel.objects.filter(email=email).exclude(id=user_id).exists():
#             raise forms.ValidationError('Этот электронный адрес уже используется!')

#         return email

class ItemModelForm(forms.ModelForm):
    date = forms.CharField(label='Дата покупки', required=False)  # Use CharField for flexible date input
    class Meta:
        model = ItemModel
        # fields = '__all__'
        
        fields= ('name','date','initial_price','residual_price','item_idx','qr_id','serial_number','company','user')
        labels={
            'name':'Название',
            'date':'Дата покупки',
            'initial_price':"Первоначальная стоимость",
            'residual_price':'Остаточная стоимость',
            'item_idx':'ID инвентаря',
            'qr_id':'QR код',
            'serial_number':'Серийный номер',
            'company':'Компания',
            'user':'Сотрудник'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the input format for the 'date' field
        #self.fields['date'].input_formats = ['%d.%m.%Y']
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
        
        self.fields['user'].empty_label='Выбрать'
        self.fields['company'].empty_label='Выбрать' 
        
        #  # Filter out inactive roles and companies
        self.fields['company'].queryset = CompanyModel.objects.filter(is_active=True)
        # self.fields['user'].queryset = User.objects.filter(is_active=True).values_list('first_name', 'last_name')
        self.fields['company'].widget.attrs.update({'class': 'company-dropdown'})
        
        self.fields['user'].initial = None
        
        self.fields['user'].choices = self.get_user_choices()
        
        
    def clean(self):
        cleaned_data = super().clean()

        numeric_fields = ['initial_price', 'residual_price']

        for field_name in numeric_fields:
            value = cleaned_data.get(field_name)
            if value is not None and str(value).lower() == 'nan':
                cleaned_data[field_name] = None

        return cleaned_data
    def clean_initial_price(self):
        return self.validate_decimal('initial_price')

    def clean_residual_price(self):
        return self.validate_decimal('residual_price')

    def validate_decimal(self, field_name):
        value = self.cleaned_data[field_name]
        if value is not None and str(value).lower() == 'nan':
            raise forms.ValidationError([f'"{value}" value must be a decimal number for the field "{field_name}"'])
        return value
    
    def clean_date(self):
        date_str = self.cleaned_data['date']
        date_obj = None

        if date_str:
            date_formats = ['%d.%m.%Y', '%Y-%m-%d']  # Add more formats as needed

            for date_format in date_formats:
                try:
                    date_obj = datetime.strptime(date_str, date_format).date()
                    break  # Stop iterating if successful
                except ValueError:
                    continue  # Try the next format

            if date_obj is None:
                raise forms.ValidationError('Invalid date format. Please use one of the following formats: DD.MM.YYYY, YYYY-MM-DD.')

        return date_obj
    
    def get_user_choices(self):
        user_choices = [(None, 'Выбрать')]
        users = User.objects.filter(is_active=True)
        for user in users:
            user_choices.append((user.id, f'{user.first_name} {user.last_name}'))
        return user_choices
    
class CompanyModelForm(forms.ModelForm):
    class Meta:
        model = CompanyModel
        # fields = '__all__'
        fields=['name']
        
        labels={
            'name':'Название компании'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = RoleModel
        # fields = '__all__'

        fields=['name']
        labels={
            'name':'Название должности'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        # fields = '__all__'

        fields=['company']
        labels={
            'company':'Компания'
        }
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Upload File'))
        
        self.fields['company'].queryset = CompanyModel.objects.filter(is_active=True)
        self.fields['company'].empty_label='Выбрать' 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


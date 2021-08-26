from django import forms

from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib.auth.models import User

from store.models import Category, Product ,ContactModel ,Customer ,Order

from adminpanel.models import *



class ProductAddForm(forms.ModelForm):
	class Meta:
		model = Product
		exclude=('submitted_at','updated_at')
		
class OrderAddForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude=('date',)

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        # exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
####
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        fields = ['name','phone']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ['username','password']

####
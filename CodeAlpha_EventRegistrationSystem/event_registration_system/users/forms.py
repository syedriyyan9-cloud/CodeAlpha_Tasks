from .models import User_Registration
from django import forms

class user_reg(forms.ModelForm):
    '''user registration form using its models'''
    class Meta:
        model = User_Registration
        fields = ['first_name','last_name','email','phone','address','city','state']
    
from django import forms
from .models import User
from django.core.exceptions import ValidationError

class CustomerCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['email','username']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("Password Doesn't match")
        return password2
    
    def save(self, commit = True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user
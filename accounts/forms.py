from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser as User
from django.core.validators import MinLengthValidator

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='')
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='')
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='')
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Phone Number", initial='')
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}), initial='')
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password", initial='', validators=[MinLengthValidator(6)])
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password", initial='')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Password and Confirm Password do not match.")
        return cleaned_data

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set user_pass to password1
        user.user_pass = self.cleaned_data.get('password1')

        if commit:
            user.save()
        return user




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
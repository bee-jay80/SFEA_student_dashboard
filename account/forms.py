from django.forms import ModelForm
from .models import CustomUser, Profile
from django import forms

class CustomUserCreationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'student_reg_no', 'password', 'role']

        # create user and make sure password is secured and not stored in plain text
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
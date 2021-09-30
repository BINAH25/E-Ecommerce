from django import forms
from .models import Order, Customer,Product
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'full_name', 'address' ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            
            
        }

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('Customer with this username already exist')
        return uname 

    def clean_email(self):
        mail = self.cleaned_data.get('email')
        if User.objects.filter(email=mail).exists():
            raise forms.ValidationError('Email already exist')
        return mail


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'multiple': True
    }))
    class Meta:
        model = Product
        fields = ['title', 'slug', 'category', 'image','marked_price', 
        'selling_price', 'description', 'return_policy', 'warranty']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product title here...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the unique slug here...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'marked_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter marked price of the product here...'
            }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter selling price of the product here...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product description here...'
            }),
            'return_policy': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the return policy here...'
            }),
            'warranty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the warranty here...'
            }),
            
            
        }

class ForgotPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email here...'
    }))
    
    def clean_email(self):
        e = self.cleaned_data.get('email')
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError('Customer with this email account does not exists..')
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password

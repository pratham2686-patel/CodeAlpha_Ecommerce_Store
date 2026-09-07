from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order
from .models import Review
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'
            if 'placeholder' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['placeholder'] = field.replace('_', ' ').title()

class OrderCreateForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'John Doe', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'john@example.com', 'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '+1 (555) 019-2834', 'class': 'form-control'}))
    address = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': '123 Main St, Apt 4B', 'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'New York', 'class': 'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'NY / California', 'class': 'form-control'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '10001', 'class': 'form-control'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'United States / India', 'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'address', 'city', 'state', 'postal_code', 'country']

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if len(full_name) < 2:
            raise forms.ValidationError("Please enter a valid full name (at least 2 characters).")
        return full_name

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        digits = [c for c in phone if c.isdigit()]
        if len(digits) < 7:
            raise forms.ValidationError("Please enter a valid phone number with at least 7-10 digits.")
        return phone

    def clean_postal_code(self):
        code = self.cleaned_data.get('postal_code', '').strip()
        if len(code) < 3:
            raise forms.ValidationError("Please enter a valid postal/ZIP code (at least 3 characters).")
        return code

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'quantity-input', 'min': '1', 'max': '100'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience with this product...'}),
        }
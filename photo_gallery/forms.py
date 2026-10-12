from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# registration 
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields=[
            'username',
            'email',
            'password1',
            'password2'
        ]
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An Account with this email exists.'
            )
        return email

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields =[
            'title',
            'desctiption',
            'image',
            'tags'
        ]
        widgets ={
            'title':forms.TextInput(attrs={
                'placeholder':'Photo Title'
            }),
            'description':forms.Textarea(attrs={
                'placeholder': 'Photo description',
                'rows':4
                
            }),
        }


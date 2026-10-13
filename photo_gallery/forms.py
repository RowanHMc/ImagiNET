from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Photo, Tag

# registration 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style all registration input fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': (
                    'w-full rounded-lg border border-gray-300 '
                    'bg-gray-50 px-4 py-3 text-gray-700 '
                    'outline-none transition '
                    'focus:border-pink-500 focus:bg-white '
                    'focus:ring-2 focus:ring-pink-100'
                )
            })

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An Account with this email exists.'
            )

        return email



class PhotoUploadForm(forms.ModelForm):
    CATEGORIES = [
        'Wildlife',
        'Nature',
        'Geography',
        'Archeology',
        'History',
        'Philosophy',
        'Technology',
        'Woodworks',
        'Construction',
        'Engineering',
        'Medicine',  

    ]
    class Meta:
        model = Photo
        fields = [
            'title',
            'description',
            'image',
            'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Photo Title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Photo description',
                'rows': 6
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['tags'].queryset = Tag.objects.filter(
            name__in=self.CATEGORIES
        ).order_by('name')
        
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': (
                    'w-full rounded-lg border border-gray-300 '
                    'bg-gray-50 px-4 py-3 text-gray-700 '
                    'outline-none transition '
                    'focus:border-pink-500 focus:bg-white '
                    'focus:ring-2 focus:ring-pink-100'
                )
            })



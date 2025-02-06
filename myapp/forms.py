from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from myapp.models import Todo

class SignUpForm(UserCreationForm):

    class Meta:

        model = User

        fields=["username","email","password1","password2"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={"class": "form-control mb-2"})
        self.fields['email'].widget = forms.EmailInput(attrs={"class": "form-control mb-2"})
        self.fields['password1'].widget = forms.PasswordInput(attrs={"class": "form-control mb-2"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={"class": "form-control mb-2"})
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class SignInForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-3"}))


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        exclude = ("created_at","owner")

        widgets = {
            "title":forms.TextInput(attrs={'class': 'form-control mb-3',
                'placeholder': 'Enter Task title'}),
            "category":forms.Select(attrs={"class":"form-control form-select mb-3"}),
            'due_date': forms.DateInput(attrs={'type': 'date',"class":"form-control mb-3"}),
            "priority":forms.Select(attrs={"class":"form-control form-select mb-3"}),
            "status":forms.Select(attrs={"class":"form-control form-select mb-3"})
        }
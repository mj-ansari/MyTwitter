from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={"placeholder": "Profile Bio", "class": "form-control"}
        ),
        required=False,
    )
    homepage_link = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Website Link", "class": "form-control"}
        ),
        required=False,
    )
    facebook_link = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Facebook Link", "class": "form-control"}
        ),
        required=False,
    )
    instagram_link = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Instagram Link", "class": "form-control"}
        ),
        required=False,
    )
    linkedin_link = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Linkedin Link", "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = Profile
        fields = (
            "profile_image",
            "profile_bio",
            "homepage_link",
            "facebook_link",
            "instagram_link",
            "linkedin_link",
        )


class TweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Enter Your Tweet Here !",
                "class": "form-control",
                "rows": 7,
            }
        ),
        label="",
    )

    class Meta:
        model = Tweet
        exclude = (
            "user",
            "likes",
        )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["username"].label = ""
        self.fields[
            "username"
        ].help_text = '<span class="form-text text-muted"><small>Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""
        self.fields[
            "password1"
        ].help_text = '<span class="form-text text-muted"><small>Password must contains at least 8 character (upper,small,number,special characters)</small></span>'

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields[
            "password2"
        ].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

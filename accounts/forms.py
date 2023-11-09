from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self): # check password and confirm password match
        cleaned_date = super(UserForm, self).clean()
        password = cleaned_date.get('password')
        confirm_password = cleaned_date.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start Typing', 'required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_picture', 'address',
                  'country', 'state', 'city', 'zip_code', 'lattitude', 'longtitude']
    
    # readonly for longtitude and latitude
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'lattitude' or field == 'longtitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
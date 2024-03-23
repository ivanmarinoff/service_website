from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from Vehicle_service.admin_user import models

UserModel = get_user_model()


class MechanicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class MechanicUpdateStatusForm(forms.Form):
    stat = (('Approved', 'Approved'), ('Repairing', 'Repairing'), ('Repairing Done', 'Repairing Done'))
    status = forms.ChoiceField(choices=stat)


class MechanicForm(forms.ModelForm):
    class Meta:
        model = models.Mechanic
        fields = ['address', 'mobile', 'profile_pic', 'skill']


class MechanicSalaryForm(forms.Form):
    salary = forms.IntegerField()

    class Meta:
        model = models.Mechanic
        fields = ['address', 'mobile', 'profile_pic', 'skill']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['by', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }

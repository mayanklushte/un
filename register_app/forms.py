from django import forms
from django.contrib.auth.models import User
from register_app.models import pat_register, doc_register, pat_details, R_appoint,pat_report



# patient form


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class Register_form(forms.ModelForm):
    Sex_choice = (('1', 'Male'),
                ('2', 'Female'),
                ('3', 'Transgender'))
    sex = forms.ChoiceField(choices=Sex_choice)


    class Meta():
        model = pat_register
        exclude = ['user']


# doctor form


class DocForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class Dregister_form(forms.ModelForm):
    TIME_CHOICES = (('00:00:00', 'Midnight'),
                    ('01:00:00', '01 AM'),
                    ('02:00:00', '02 AM'),
                    ('03:00:00', '03 AM'),
                    ('04:00:00', '04 AM'),
                    ('05:00:00', '05 AM'),
                    ('06:00:00', '06 AM'),
                    ('07:00:00', '07 AM'),
                    ('08:00:00', '08 AM'),
                    ('09:00:00', '09 AM'),
                    ('10:00:00', '10 AM'),
                    ('11:00:00', '11 AM'),
                    ('12:00:00', 'Noon'),
                    ('13:00:00', '01 PM'),
                    ('14:00:00', '02 PM'),
                    ('15:00:00', '03 PM'),
                    ('16:00:00', '04 PM'),
                    ('17:00:00', '05 PM'),
                    ('18:00:00', '06 PM'),
                    ('19:00:00', '07 PM'),
                    ('20:00:00', '08 PM'),
                    ('21:00:00', '09 PM'),
                    ('22:00:00', '10 PM'),
                    ('23:00:00', '11 PM'),)

    Day_choice=(('Sunday','Sunday'),
                ('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'),
                ('Friday', 'Friday'),
                ('Saturday', 'Saturday'))

    Sex_choice = (('1', 'Male'),
                  ('2', 'Female'),
                  ('3', 'Transgender'))

    sex = forms.ChoiceField(choices=Sex_choice)
    open_time = forms.ChoiceField(choices=TIME_CHOICES)
    close_time = forms.ChoiceField(choices=TIME_CHOICES)
    close_day = forms.ChoiceField(choices=Day_choice)

    class Meta():
        model = doc_register
        exclude = ['user']


class AppointmentForm(forms.ModelForm):

    TIME_CHOICES = (('00:00:00', 'Midnight'),
                    ('01:00:00', '01 AM'),
                    ('02:00:00', '02 AM'),
                    ('03:00:00', '03 AM'),
                    ('04:00:00', '04 AM'),
                    ('05:00:00', '05 AM'),
                    ('06:00:00', '06 AM'),
                    ('07:00:00', '07 AM'),
                    ('08:00:00', '08 AM'),
                    ('09:00:00', '09 AM'),
                    ('10:00:00', '10 AM'),
                    ('11:00:00', '11 AM'),
                    ('12:00:00', 'Noon'),
                    ('13:00:00', '01 PM'),
                    ('14:00:00', '02 PM'),
                    ('15:00:00', '03 PM'),
                    ('16:00:00', '04 PM'),
                    ('17:00:00', '05 PM'),
                    ('18:00:00', '06 PM'),
                    ('19:00:00', '07 PM'),
                    ('20:00:00', '08 PM'),
                    ('21:00:00', '09 PM'),
                    ('22:00:00', '10 PM'),
                    ('23:00:00', '11 PM'),)
    Appointment_Date = forms.DateField(widget=forms.SelectDateWidget(attrs={'size': '1','class': 'special'}))
    Appointment_Time = forms.ChoiceField(choices=TIME_CHOICES)

    class Meta:
        model = R_appoint
        fields = ("Appointment_Date", "Appointment_Time", "Mobile_Number")


class pat_detail_form(forms.ModelForm):

    class Meta:
        model = pat_details
        fields = ("symptoms", "medical_history", "examination", "diagnosis", "medication_list", "fee")


class report_form(forms.ModelForm):

    class Meta:
        model = pat_report
        fields = ("X_ray", "MRI", "CT_Scan", "ECG", "Blood_test")


class InputForm(forms.Form):

    x = forms.IntegerField(label='Weight')
    y = forms.IntegerField(label='Height')
    z = forms.IntegerField(label='Age')


class BMIForm(forms.Form):

    x = forms.IntegerField(label='Weight')
    y = forms.IntegerField(label='Height')


class TBWForm(forms.Form):

    x = forms.IntegerField(label='Weight')
    y = forms.IntegerField(label='Height')
    z = forms.IntegerField(label='Age')

class TBW_FForm(forms.Form):

    x = forms.IntegerField(label='Weight')
    y = forms.IntegerField(label='Height')


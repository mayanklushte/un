from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



class pat_register(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    moblie_no = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10)
    profile_photo = models.ImageField(upload_to='profile_pic',blank=True)

    def __str__(self):
        return self.user.first_name


class doc_register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    moblie_no = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10)
    clinic_phone_no = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{1,10}$')])
    specialist = models.CharField(max_length=20)
    open_time = models.TimeField()
    close_time = models.TimeField()
    close_day = models.CharField(max_length=12)
    profile_photo = models.ImageField(upload_to='profile_pic',blank=True)

    def __str__(self):
        return self.user.first_name


class R_appoint(models.Model):
    Doctor_Name = models.ForeignKey(doc_register, on_delete=models.CASCADE)
    Patient_Name = models.ForeignKey(pat_register, related_name='users', on_delete=models.CASCADE)
    Appointment_Date = models.DateField(auto_now_add=False)
    Appointment_Time = models.TimeField()
    Mobile_Number = models.CharField(max_length=10)
    status = models.NullBooleanField()

    def __str__(self):
        return self.Patient_Name


class pat_details(models.Model):
    Patient_name = models.ForeignKey('pat_register',on_delete=models.CASCADE)
    Doctor_name=models.ForeignKey('doc_register',on_delete=models.CASCADE, related_name='doc')
    symptoms = models.CharField(max_length=500)
    medical_history = models.CharField(max_length=500)
    examination = models.CharField(max_length=500)
    diagnosis = models.CharField(max_length=500)
    medication_list = models.CharField(max_length=500)
    fee = models.CharField(max_length=7)
    appoin_time = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Patient_name


class pat_report(models.Model):
    pat_details=models.ForeignKey('pat_details',on_delete=models.CASCADE, related_name='sum')
    Patient_name = models.ForeignKey('pat_register', on_delete=models.CASCADE)
    Doctor_name = models.ForeignKey('doc_register', on_delete=models.CASCADE, related_name='ren')
    X_ray = models.FileField(upload_to='x_ray',blank=True,default='x_ray/sample.png')
    MRI= models.FileField(upload_to='mri',blank=True, default='mri/sample.png')
    CT_Scan = models.FileField(upload_to='ct_scan',blank=True,default='ct_scan/sample.png')
    ECG = models.FileField(upload_to='ecg',blank=True,default='bd_test/sample.png')
    Blood_test = models.FileField(upload_to='bd_test',blank=True,default='bd_test/sample.png')

    def __str__(self):
        return self.pat_details

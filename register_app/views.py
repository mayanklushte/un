from django.shortcuts import render
from register_app.forms import Register_form, UserForm

from register_app.forms import *
from register_app.models import pat_register, doc_register, R_appoint, pat_details
from django.http import Http404
from django.db.models import Q, Count
from django.db.models import Value
from django.db.models.functions import Concat
import datetime
from datetime import date
from datetime import timedelta
from django.utils import timezone



# Create your views here.

# extra imports for login authentification

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'login_app/index.html')


def u_pat(request):
    return render(request, 'register_app/user1.html')


@login_required
def special(request):
    return HttpResponse("You are logged in. Nice!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def users(request):

    registered = False

    if request.method == 'POST':

        form_p = UserForm(data=request.POST)
        form = Register_form(data=request.POST)

        if form.is_valid() and form_p.is_valid():

            user = form_p.save()
            user.set_password(user.password)
            user.save()

            form_r = form.save(commit=False)
            form_r.user = user  # here connected OneToOneField with user table

            if 'profile_photo' in request.FILES:
                form_r.profile_photo = request.FILES['profile_photo']

            form_r.save()

            registered = True
        else:
            print(form_p.errors, form.errors)
    else:
        form_p = UserForm()
        form = Register_form()

    return render(request, 'register_app/register_page.html', {'form': form,
                                                               'form_p': form_p,
                                                               'registered': registered})

# login page view


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('register_app:h_doc'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'register_app/login.html', {})

# doctor views start here


@login_required
def doc_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def doc_users(request):

    registered = False

    if request.method == 'POST':

        form_d = DocForm(data=request.POST)  # form_d is for doctor form inheritaed from user table(form_p=form_d)
        d_form = Dregister_form(data=request.POST)  # d_form is for newly created form for registration(form=d_form)
        if d_form.is_valid() and form_d.is_valid():

            user = form_d.save()
            user.set_password(user.password)
            user.save()

            form_rd = d_form.save(commit=False)  # form_r=form_rd
            form_rd.user = user  # here connected OneToOneField with user table

            if 'profile_photo' in request.FILES:
                form_rd.profile_photo = request.FILES['profile_photo']

            form_rd.save()

            registered = True
        else:
            print(form_d.errors, d_form.errors)
    else:
        form_d = DocForm()
        d_form = Dregister_form()

    return render(request, 'register_app/doc_register.html', {'d_form': d_form,
                                                              'form_d': form_d,
                                                              'registered': registered})

# doc login page view


def doc_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('register_app:acc_app'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'register_app/doc_login.html', {})



# for doctor


@login_required
def pat_list(request):
    a = doc_register.objects.get(user_id__exact=request.user)
    all_patient = R_appoint.objects.filter(Q(Doctor_Name_id=a))
    return render(request, 'register_app/user.html', {'all_patient': all_patient })


@login_required
def pat_detail(request, id):
    try:
        user = pat_register.objects.get(pk=id)
        user1 = pat_register.objects.all()
    except pat_register.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/details.html', {'user': user}, {'user1': user1})


@login_required
def pat_detail_form_view(request, id):

    pj = pat_register.objects.get(id=id)
    a = doc_register.objects.get(user_id=request.user)

    if request.method == 'POST':

        pat_dat = pat_detail_form(data=request.POST)

        if pat_dat.is_valid():

            dat = pat_dat.save(commit=False)
            dat.Patient_name_id = pj.pk
            dat.Doctor_name_id = a.id
            dat.save(True)

            return HttpResponseRedirect(reverse('register_app:acc_app'))
        else:
            print(pat_dat.errors)
    else:
        pat_dat = pat_detail_form()
    return render(request, 'register_app/pat_detail.html', {'pat_dat': pat_dat})

# for patient


@login_required
def doc_list(request):
    all_docter = doc_register.objects.all()
    return render(request, 'register_app/user1.html', {'all_docter': all_docter, })


@login_required
def search(request):
    search_term = ''
    result = doc_register.objects.annotate(search_name=Concat('user__first_name', Value(' '),
                                                              'user__last_name', Value(' '),
                                                              'address', Value(' '), 'specialist'))
    if 'search' in request.GET:
        search_term = request.GET['search']
        result = result.filter(search_name__icontains=search_term)
    return render(request, 'register_app/search.html', {'result': result, 'search_term': search_term})


@login_required
def d_detail1(request, id):
    try:
        d_user = doc_register.objects.get(pk=id)
        d_user1 = doc_register.objects.all()
    except doc_register.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/d_details.html', {'d_user': d_user}, {'d_user1': d_user1})


# appointment

@login_required
def p_appoint(request, id):
    rj = doc_register.objects.get(id=id)
    a = pat_register.objects.get(user_id=request.user)

    if request.method == 'POST':

        appoint = AppointmentForm(data=request.POST)





        if appoint.is_valid():

            random = appoint.save(commit=False)
            random.Doctor_Name_id = rj.pk
            random.Patient_Name_id = a.id
            random.save(True)

            return HttpResponseRedirect(reverse('register_app:search'))
        else:
            print(appoint.errors)
    else:
        appoint = AppointmentForm()
    return render(request, 'register_app/Appointmnet.html', {'appoint': appoint})


@login_required
def appoint_list(request):
        try:
            a = doc_register.objects.get(user_id__exact=request.user)
            lists = R_appoint.objects.filter(Q(Doctor_Name=a)).filter(Q(status=None))
        except R_appoint.DoesNotExist:
            raise Http404("")
        return render(request, 'register_app/p_list.html', {'lists': lists})


@login_required
def appoint_list1(request, id):
        try:
            listsq = R_appoint.objects.get(id=id)

        except R_appoint.DoesNotExist:
            raise Http404("")
        return render(request, 'register_app/ap_detail.html', {'listsq': listsq})


@login_required
def accept(request, id):
        try:
            listsz = R_appoint.objects.get(id=id)
            listsz.status = True
            listsz.save()
            if listsz.status==True:
                return HttpResponseRedirect(reverse('register_app:u_appoint'))

        except R_appoint.DoesNotExist:
            raise Http404("")

        return render (request, 'register_app/ap_detail.html', {'listsz': listsz})

@login_required
def reject(request, id):
    try:
        listsy = R_appoint.objects.get(id=id)
        listsy.status = False
        listsy.save()
        if listsy.status==False:
            return HttpResponseRedirect(reverse('register_app:u_appoint'))

    except R_appoint.DoesNotExist:
        raise Http404("")

    return render(request, 'register_app/ap_detail.html', {'listsy': listsy})


@login_required
def req_stat(request):
    try:
        check = pat_register.objects.get(user_id__exact=request.user)
        check1= R_appoint.objects.filter(Q(Patient_Name=check)).filter(Q(status=True)).order_by('Appointment_Date').filter(Q(Appointment_Date__gte=date.today()))
        check2 = R_appoint.objects.filter(Q(Patient_Name=check)).filter(Q(status=False)).order_by(
            'Appointment_Date').filter(Q(Appointment_Date__gte=date.today()))

    except R_appoint.DoesNotExist:
        raise Http404("")
    return render (request, 'register_app/req_stat.html', {'check1':check1, 'check2': check2})


@login_required
def acc_list(request):
    try:
        a = doc_register.objects.get(user_id__exact=request.user)
        lists1 = R_appoint.objects.filter(Q(Doctor_Name=a)).filter(Q(status=True)).order_by('Appointment_Date').filter(Q(Appointment_Date=date.today()))
    except R_appoint.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/acc_list.html', {'lists1': lists1})


@login_required
def acc_list_tomo(request):
    try:
        a = doc_register.objects.get(user_id__exact=request.user)
        lists1 = R_appoint.objects.filter(Q(Doctor_Name=a)).filter(Q(status=True)).order_by('Appointment_Date').filter(Q(Appointment_Date=timezone.now()+datetime.timedelta(1)))
    except R_appoint.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/acc_list_tomo.html', {'lists1': lists1})


@login_required
def appoint_list2(request):
    try:
        a = pat_register.objects.get(user_id__exact=request.user)
        lists1 = R_appoint.objects.filter(Q(Patient_Name=a)).filter(Q(status=True)).order_by('Appointment_Date').filter(Q(Appointment_Date=date.today()))
        lists2 = R_appoint.objects.filter(Q(Patient_Name=a)).filter(Q(status=True)).filter(Q(Appointment_Date=timezone.now() + datetime.timedelta(1)))
    except R_appoint.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/pl_list.html', {'lists1': lists1,'lists2':lists2})



@login_required
def pat_info(request, id):
    try:
        user = R_appoint.objects.get(pk=id)
        user1 = pat_register.objects.get(Q(pk=user.Patient_Name_id))
        user4 = R_appoint.objects.filter(pk=user.pk)
        user3 = doc_register.objects.get(Q(pk=user.Doctor_Name_id))
        user2 = pat_details.objects.filter(Q(Patient_name_id=user1.pk)).filter(Q(Doctor_name_id=user3.pk))

    except pat_register.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/pat_info.html', {'user1': user1, 'user': user, 'user2': user2, 'user4': user4})


@login_required
def H_doc_list(request):
    try:

        a = pat_register.objects.get(user_id__exact=request.user)
        lists1 = R_appoint.objects.filter(Q(Patient_Name=a)).filter(Q(status=True))
    except R_appoint.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/p_acc_list.html', {'lists1': lists1})


@login_required
def pat_pat_info(request, id):
    try:
        user = R_appoint.objects.get(pk=id)
        user4 = R_appoint.objects.filter(pk=user.pk)
        user1 = doc_register.objects.get(Q(id=user.Doctor_Name_id))
        user3 = pat_register.objects.get(Q(user_id__exact=request.user))
        user2 = pat_details.objects.filter(Q(Patient_name_id=user3.id)).filter(Q(Doctor_name_id=user1.id))
        user5 = pat_report.objects.filter(Q(Patient_name_id=user3.id)).filter(Q(Doctor_name_id=user1.id))

    except pat_register.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/pat_pat_info.html', {'user1': user1,'user3':user3, 'user': user,'user2':user2, 'user4':user4, 'user5': user5 })

@login_required
def pat_report_view(request, id):
    try:
        user1 = pat_details.objects.get(pk=id)
        user2 = pat_report.objects.filter(Q(pat_details_id__exact=user1.id))
    except pat_report.DoesNotExist:
        raise Http404("")
    return render(request, 'register_app/pat_report.html', {'user2': user2 })

@login_required
def report_view(request, id):

    a = pat_register.objects.get(user_id=request.user)
    b = pat_details.objects.get(id=id)

    if request.method == 'POST':

        report = report_form(request.POST, request.FILES)

        if report.is_valid():

            random = report.save(commit=False)
            random.Doctor_name_id = b.Doctor_name_id
            random.Patient_name_id = a.pk
            random.pat_details_id = b.pk

            random.save(True)

            return HttpResponseRedirect(reverse('register_app:h_doc'))
        else:
            print(report.errors)
    else:
        report = report_form()
    return render(request, 'register_app/report.html', {'report': report})



def add(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            input1 = cd['x']
            input2 = cd['y']
            input3 = cd['z']

            output = 10*input1+6.25*input2-5*input3-161
            # Save the result in the session
            request.session['output'] = output
            return HttpResponseRedirect('thanks/')
    else:
        form = InputForm()
    return render(request, 'register_app/input.html', {'form': form})


def thanks(request):
    # Get the result from the session
    output = request.session.pop('output', None)
    return render(request, 'register_app/output.html', {'output': output})


def M_input(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            input1 = cd['x']
            input2 = cd['y']
            input3 = cd['z']

            output = 10*input1+6.25*input2-5*input3+5
            # Save the result in the session
            request.session['output'] = output
            return HttpResponseRedirect('M_thanks/')
    else:
        form = InputForm()
    return render(request, 'register_app/M_input.html', {'form': form})


def M_thanks(request):
    # Get the result from the session
    output = request.session.pop('output', None)
    return render(request, 'register_app/M_output.html', {'output': output})


def BMI(request):
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            input1 = cd['x']
            input2 = cd['y']

            output = input1/(input2*input2)*10000
            # Save the result in the session
            request.session['output'] = output
            return HttpResponseRedirect('BMI_O/')
    else:
        form = BMIForm()
    return render(request, 'register_app/BMI.html', {'form': form})


def BMI_O(request):
    # Get the result from the session
    output = request.session.pop('output', None)
    return render(request, 'register_app/BMI_O.html', {'output': output})


def TBW(request):
    if request.method == 'POST':
        form = TBWForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            input1 = cd['x']
            input2 = cd['y']
            input3 = cd['z']

            output = (2.447 - 0.09156 * input3)+(0.1074 * input2) + (0.3362 * input1)
            # Save the result in the session
            request.session['output'] = output
            return HttpResponseRedirect('TBW_O/')
    else:
        form = TBWForm()
    return render(request, 'register_app/TBW.html', {'form': form})


def TBW_O(request):
    # Get the result from the session
    output = request.session.pop('output', None)
    return render(request, 'register_app/TBW_O.html', {'output': output})


def TBW_F(request):
    if request.method == 'POST':
        form = TBW_FForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            input1 = cd['x']
            input2 = cd['y']

            output = (-2.097 + 0.1069 * input2) + (0.2466 * input1)
            # Save the result in the session
            request.session['output'] = output
            return HttpResponseRedirect('TBW_OF/')
    else:
        form = TBW_FForm()
    return render(request, 'register_app/TBW_F.html', {'form': form})


def TBW_OF(request):
    # Get the result from the session
    output = request.session.pop('output', None)
    return render(request, 'register_app/TBW_OF.html', {'output': output})


from django.http import HttpResponse
from django.views.generic import View
from register_app.utils import render_to_pdf #created in step 4
from django.template.loader import get_template


class GeneratePdf(View):
    def get(self, request, id):

        list = pat_details.objects.get(Q(id=id))
        data = {
            'today': datetime.date.today(),
            'symptoms': list.symptoms,
            'TEL': list.Doctor_name.clinic_phone_no,
            'doc_add': list.Doctor_name.address,
            'Patient_name': list.Patient_name.user.first_name,
            'last_name': list.Patient_name.user.last_name,
            'profile_photo': list.Patient_name.profile_photo.url,
            'pin':list.Doctor_name.pincode,
            'open':list.Doctor_name.open_time,
            'close': list.Doctor_name.close_time,
            'c_day': list.Doctor_name.close_day,
            'ap_time': list.appoin_time,
            'p_mh': list.medical_history,
            'p_medl':list.medication_list,
            'p_e':list.examination,
            'p_d':list.diagnosis,
            'p_f':list.fee,
            'D_N':list.Doctor_name.user.first_name,
            'D_L':list.Doctor_name.user.last_name
        }
        pdf = render_to_pdf('register_app/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


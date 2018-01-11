from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .models import *
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.db.models import Count


def user_login(request):
    """
    Checks if the user submitted a form
    If the request is a POST take the post data and and check if they have been filled out.
    Further... if the user is not logged in and tries to make a request against a protected route
    they will be redirected and the next key word will go into play.
    """

    if request.user.is_authenticated():
        return redirect('base_dashboard')

    if request.POST:
        next_redirect = request.POST.get('next')
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        if not all([password, username]):
            messages.add_message(request, messages.ERROR, 'Please enter username & password')
            return redirect('user_login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.add_message(request, messages.ERROR, 'Incorrect Username/Password')
            return redirect('user_login')

        login(request, user)

        if next_redirect:
            return redirect(next_redirect)

        return redirect('base_dashboard')

    return render(request, 'login.html')


def create_account(request):
    """
    This form takes the post data and creates the entire user profile such as medical information
    insurance information and so on.
    """
    if request.POST:
        try:
            username, password = create_account_form(request, request.POST)

            user = authenticate(username=username, password=password)
            if user is None:
                messages.add_message(request, messages.ERROR, 'Oops! Something went wrong.')
                hospitals = Hospital.objects.all()
                return render(request, 'create_account.html', {'hospitals': hospitals})
            login(request, user)
            return redirect('base_dashboard')
        except ValueError:
            pass

    hospitals = Hospital.objects.all()

    return render(request, 'create_account.html', {'hospitals': hospitals})


def create_account_form(request, post):
    """
    This is the method that actually handles the authentication and login functions which are
    the default django authentication system.
    """
    username = post.get("username")
    first_name = post.get("first_name")
    last_name = post.get("last_name")
    email = post.get("email")

    phone_number = post.get("phone")

    password = post.get("password")

    height = float(post.get("height"))
    weight = float(post.get("weight"))
    sex = post.get("sex")

    current_medications = post.get("medications")
    allergies = post.get("allergies")
    medical_conditions = post.get("medical_conditions")
    family_history = post.get("family_history")
    additional_info = post.get("additional_info")
    primary_hospital = Hospital.objects.get(pk=post.get("primary_hospital"))

    policy_number = int(post.get("policy_number"))
    company = post.get("company")

    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, 'User already exists!')
        return False

    else:
        new_user = User.objects.create_user(
            username=username, password=password,
            first_name=first_name, last_name=last_name, email=email
        )

        new_user_profile = UserProfile.objects.create(
            user=new_user,
            phone_number=phone_number, status=UserStatus.objects.get(pk=3),
            primary_hospital=primary_hospital
        )

        medical_info = MedicalInformation.objects.create(
            height=height, weight=weight, sex=sex,
            medical_conditions=medical_conditions,
            allergies=allergies, medications=current_medications,
            family_history=family_history, additional_info=additional_info,
            user=new_user_profile
        )

        insurance = Insurance.objects.create(
            policy_number=policy_number, company=company, medical_information=medical_info,
        )

    return True


@login_required
def log_out(request):
    """
    This flushes out the user object from the session which in turn logs the user out.
    """
    logout(request)
    return redirect('user_login')


@login_required
def base_dashboard(request):
    """
    This is the system that first includes the specific dashboards based on what type the user is.
    """
    appointments = None

    if request.user.userprofile.is_patient():
        appointments = Appointment.objects.filter(patient=request.user.id).order_by('date')
    elif request.user.userprofile.is_doctor():
        appointments = Appointment.objects.filter(doctor=request.user.id).order_by('date')
    else:
        appointments = Appointment.objects.all().order_by('date')

    return render(request, 'base_dashboard.html', {'appointments': appointments, 'the_user': request.user})


def create_appointment(request):
    """
   This function creates an appointment but however it is ill-implemented.
   """
    dates = get_dates()
    users = User.objects.all()

    if request.POST:
        new_appointment = create_appointment_form(request, request.POST)
        if new_appointment:
            messages.add_message(request, messages.SUCCESS, 'Your appointment as been created successfully.')
        else:
            messages.add_message(request, messages.ERROR, 'An error occurred. Your appointment could not be created.'
                                                          'If this error persists, try contacting our service desk at'
                                                          '1-800-RIX-AJAZ')
        return redirect('view_appointments')

    return render(request, 'create_appointment.html', {'the_user': request.user,
                                                       'dates': dates,
                                                       'users': users,
                                                       'hours': range(1, 13),
                                                       'minutes': range(1, 60)})


def get_dates():
    """
    Helper function to get dates in an iterrable way.
    """
    return {
        "years": range(datetime.date.today().year, datetime.date.today().year + 5),
        "months": range(1, 13),
        "days": range(1, 32)
    }


def create_appointment_form(request, post):
    """
   This code creates a new appoint object. Based on what type of user it is the
   user can either be a doctor or a patient.
   """
    # string_date = "{0}-{1}-{2}".format(year, month, day)
    # date = datetime.datetime.strptime(string_date, '%Y-%m-%d').date()
    new_appointment = None
    date_string = post.get("date") + "-" + post.get("time")
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d-%H:%M')
    the_user = request.user
    notes = post.get("notes")

    if the_user.userprofile.is_doctor():
        patient_id = int(post.get("patient", the_user.pk))
        patient = User.objects.get(pk=patient_id)
        doctor = User.objects.get(pk=the_user.id)
        new_appointment = Appointment.objects.create(date=date, doctor=doctor, patient=patient, notes=notes)

    elif request.user.userprofile.is_patient():
        doctor_id = int(post.get("doctor", the_user.pk))
        doctor = User.objects.get(pk=doctor_id)
        patient = User.objects.get(pk=the_user.id)
        new_appointment = Appointment.objects.create(date=date, doctor=doctor, patient=patient, notes=notes)

    return new_appointment


@login_required
def view_appointments(request):
    """
   This method shows all appointments specifically if your a patient.
    """

    appointments = Appointment.objects.all().order_by('date')

    if request.user.userprofile.is_patient():
        appointments = Appointment.objects.filter(patient=request.user.id).order_by('date')

    elif request.user.userprofile.is_doctor():
        appointments = Appointment.objects.filter(doctor=request.user.id).order_by('date')

    return render(request, 'view_appointments.html', {'appointments': appointments,
                                                      'the_user': request.user})


def edit_appointment(request, id):
    """
    The edit appointment method allows user to edit an appointment
    """
    users = User.objects.all()
    appointment = get_object_or_404(Appointment, pk=id)
    if request.POST:
        post = request.POST
        date_string = post.get("date") + "-" + post.get("time")
        try:
            date = datetime.datetime.strptime(date_string, '%Y-%m-%d-%H:%M')
            appointment.date = date
        except ValueError:
            pass
        the_user = request.user
        notes = post.get("notes")
        appointment.notes = notes

        if the_user.userprofile.is_doctor():
            try:
                patient_id = int(post.get("patient", the_user.pk))
                patient = User.objects.get(pk=patient_id)
                appointment.patient = patient
            except ValueError:
                pass

        elif request.user.userprofile.is_patient():
            try:
                doctor_id = int(post.get("doctor", the_user.pk))
                doctor = User.objects.get(pk=doctor_id)
                appointment.doctor = doctor
            except ValueError:
                pass

        if appointment:
            messages.add_message(request, messages.SUCCESS, 'Your changes have been saved.')
        else:
            messages.add_message(request, messages.ERROR, 'An error occurred. Please contact an admin for assistance.')
        appointment.save()
        return redirect('view_appointments')
    return render(request, 'edit_appointment.html', {'appointment': appointment,
                                                     'the_user': request.user,
                                                     'users': users})


@login_required
def cancel_appointment(request, id):
    """
    The cancel appointment asks users if they are sure they want to cancel an appointment.
    If so, the appointment is deleted.
    """
    appointment = get_object_or_404(Appointment, pk=id)

    if request.POST:
        appointment.delete()
        messages.add_message(request, messages.SUCCESS, 'The appointment has been canceled successfully.')
        return redirect('view_appointments')

    return render(request, 'cancel_appointment.html', {'appointment': appointment})


@login_required
def edit_basic_info(request):
    """
    This method will take basic information such as last, first and email.
    """
    if request.POST:
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.email = request.POST['email']
        request.user.save()
        request.user.userprofile.phone_number = request.POST['phone']
        request.user.userprofile.save()
        messages.add_message(request, messages.SUCCESS, 'Your changes have been saved.')
        return redirect('base_dashboard')

    return render(request, 'edit_basic_info.html', {'the_user': request.user})


@login_required
def edit_medical_info(request):
    """
    This method will update the medical information for the patient.
    """
    if request.POST:
        post = request.POST
        the_user = request.user
        the_user.userprofile.medicalinformation.height = float(post.get("height"))
        the_user.userprofile.medicalinformation.weight = float(post.get("weight"))
        the_user.userprofile.medicalinformation.sex = post.get("sex")
        the_user.userprofile.medicalinformation.medications = post.get("medications")
        the_user.userprofile.medicalinformation.allergies = post.get("allergies")
        the_user.userprofile.medicalinformation.medical_conditions = post.get("medical_conditions")
        the_user.userprofile.medicalinformation.family_history = post.get("family_history")
        the_user.userprofile.medicalinformation.additional_info = post.get("additional_info")
        the_user.userprofile.medicalinformation.primary_hospital = Hospital.objects.get(pk=post.get("primary_hospital"))
        the_user.userprofile.medicalinformation.save()
        messages.add_message(request, messages.SUCCESS, 'Your changes have been saved.')
        return redirect('base_dashboard')

    hospitals = Hospital.objects.all()
    return render(request, 'edit_medical_info.html', {'the_user': request.user, 'hospitals': hospitals})


@login_required
def view_insurances(request):
    """
    This will show views of the insurance providers available to the user.
    There can be multiple insurance providers/policy numbers for a user.
    """
    insurance = Insurance.objects.filter(medical_information=request.user.userprofile.medicalinformation)
    return render(request, 'view_insurances.html', {'insurances': insurance})


@login_required
def view_insurance(request, insurance_id):
    if request.POST:
        post = request.POST
        insurance = Insurance.objects.get(pk=insurance_id)
        insurance.policy_number = post.get("policy_number")
        insurance.company = post.get("company")
        insurance.save()

        return redirect('view_insurance', insurance_id=insurance_id)

    insurance = Insurance.objects.get(pk=insurance_id)
    return render(request, 'view_insurance.html', {'insurance': insurance})


@login_required
def add_hospital(request):
    """
    This adds a new hospital to the system.
    """
    if request.POST:
        post = request.POST
        name = post.get("name")
        address = post.get("address")
        city = post.get("city")
        state = post.get("state")
        zip = post.get("zip")
        hospital = Hospital.objects.create(
            name=name,
            address=address,
            city=city,
            state=state,
            zip=zip
        )

        if hospital:
            return redirect('add_hospital')

    return render(request, 'add_hospital.html')


@login_required
def add_doctor(request):
    """
    This adds a new user of the type doctor
    """
    if request.POST:
        post = request.POST
        username = post.get("username")
        first_name = post.get("first_name")
        last_name = post.get("last_name")
        email = post.get("email")
        password = post.get("password")
        chosen_hospitals = post.getlist("chosen_hospitals")

        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        new_user_profile = UserProfile.objects.create(
            user=new_user,
            status=UserStatus.objects.get(pk=1)
        )

        if new_user:
            for chosen_hospital in chosen_hospitals:
                HospitalStaff.objects.create(user_profile=new_user_profile, hospital=Hospital.objects.get(pk=chosen_hospital))

            return redirect('add_doctor')

    hospitals = Hospital.objects.all()
    return render(request, 'add_doctor.html', {'hospitals': hospitals})


@login_required
def add_nurse(request):
    """
    This method will add a new nurse to the system.
    """
    if request.POST:
        post = request.POST
        username = post.get("username")
        first_name = post.get("first_name")
        last_name = post.get("last_name")
        email = post.get("email")
        password = post.get("password")
        chosen_hospitals = post.getlist("chosen_hospitals")

        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        new_user_profile = UserProfile.objects.create(
            user=new_user,
            status=UserStatus.objects.get(pk=2)
        )

        if new_user:
            for chosen_hospital in chosen_hospitals:
                HospitalStaff.objects.create(user_profile=new_user_profile, hospital=Hospital.objects.get(pk=chosen_hospital))

            return redirect('add_nurse')

    hospitals = Hospital.objects.all()
    return render(request, 'add_nurse.html', {'hospitals': hospitals})


@login_required
def add_admin(request):
    """
    This will add an admin user to the system.
    """
    if request.POST:
        post = request.POST
        username = post.get("username")
        first_name = post.get("first_name")
        last_name = post.get("last_name")
        email = post.get("email")
        password = post.get("password")
        chosen_hospitals = post.getlist("chosen_hospitals")

        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        new_user_profile = UserProfile.objects.create(
            user=new_user,
            status=UserStatus.objects.get(pk=4)
        )

        if new_user and new_user_profile:
            for chosen_hospital in chosen_hospitals:
                HospitalStaff.objects.create(user_profile=new_user_profile, hospital=Hospital.objects.get(pk=chosen_hospital))

            return redirect('add_admin')

    hospitals = Hospital.objects.all()

    return render(request, 'add_admin.html', {'hospitals': hospitals})


@login_required
def message_center(request, url):
    """View the message center"""

    if request.POST and url is not 'sent':
        message = Message.objects.get(id=request.POST.get("message_id"))
        if message.read:
            message.read = 0
            message.save()
        else:
            message.read = 1
            message.save()

    all_messages = Message.objects.all().order_by("-time")
    user_messages = []
    section = "all"
    if url is 'read':
        section = "read"
        for m in all_messages:
            if m.user_to.__str__() in request.user.userprofile.get_full_name() and m.read:
                user_messages.append(m)

    elif url is 'unread':
        section = "unread"
        for m in all_messages:
            if m.user_to.__str__() in request.user.userprofile.get_full_name() and not m.read:
                user_messages.append(m)

    elif url is 'sent':
        section = "sent"
        for m in all_messages:
            if m.user_from.__str__() in request.user.userprofile.get_full_name():
                user_messages.append(m)

    elif url is 'all':
        for m in all_messages:
            if m.user_to.__str__() in request.user.userprofile.get_full_name():
                user_messages.append(m)

    elif url is 'compose':
        section = 'compose'

    the_users = UserProfile.objects.exclude(user=request.user)

    return render(request, 'message_center.html', {'msgs': user_messages, 'the_users': the_users,
                                                   'display': section})


@login_required
def view_message(request, message_id):
    message = Message.objects.get(pk=message_id)

    return render(request, 'view_message.html', {'msg': message})


@login_required
def delete_message(request, message_id):
    message = Message.objects.get(pk=message_id)

    if request.POST:
        message.delete()
        messages.add_message(request, messages.SUCCESS, 'The message has been deleted.')
        return redirect('message_center')

    return render(request, 'view_message.html', {'msg': message})


@login_required
def send_message(request):
    if request.POST:
        post = request.POST

        user_from = request.user.userprofile
        user_to = UserProfile.objects.get(id=post.get("user_to"))
        subject = post.get("subject")
        message = post.get("\nmessage")

        message_created = Message.objects.create(user_from=user_from, user_to=user_to,
                                                 subject=subject, message=message,
                                                 time=timezone.now(), read=0)

        if message_created:
            messages.add_message(request, messages.SUCCESS, 'Your message has been sent.')
            return redirect('sent')

    return render(request, 'message_center.html')


@login_required
def reply_to_message(request, message_id):
    message = Message.objects.get(pk=message_id)
    line = '-----------------------------------------------------------------\n'
    orig = '---------------------- Original Message: ---------------------\n'
    fr = 'From: ' + message.user_from.get_full_name() + '\n'
    sub = 'Subject: ' + message.subject + '\n'
    content = message.message + '\n'
    stub = '[ Enter your reply here ]\n\n\n\n' + line + orig + line + fr + sub + content

    if request.POST:
        post = request.POST

        user_from = message.user_to
        user_to = message.user_from
        subject = 'RE: ' + message.subject
        message = '\n' + post.get("message")

        message_created = Message.objects.create(user_from=user_from, user_to=user_to,
                                                 subject=subject, message=message,
                                                 time=timezone.now(), read=0)

        if message_created:
            messages.add_message(request, messages.SUCCESS, 'Your reply has been sent.')
            return redirect('sent')

    return render(request, 'reply_to_message.html', {'msg': message, 'stub': stub})


@login_required
def update_message(request, message_id):
    message = Message.objects.get(id=message_id)
    if message.read:
        message.read = 0
    else:
        message.read = 1

    return redirect('all')


@login_required
def view_logs(request):
    """View the system logs """
    keyword = None
    num_logs = 0
    logs = LogEntry.objects.all()
    if request.POST:
        keyword = request.POST.get("search")
        if keyword:
            logs = []
            for log in LogEntry.objects.all():
                if keyword in log.__str__() or keyword in log.user.__str__():
                    logs.append(log)
                    num_logs += 1

    return render(request, 'view_logs.html', {'logs': logs, "keyword": keyword, "num_logs": num_logs})


@login_required
def view_log(request, log_id):
    """Delete the system log"""

    if request.POST:
        LogEntry.objects.filter(pk=log_id).delete()
        return redirect('view_logs')

    log = LogEntry.objects.get(pk=log_id)
    return render(request, 'view_log.html', {'log': log})


@login_required
def view_all_patients(request):
    keyword = None
    num_patients = 0
    all_patients = UserProfile.objects.filter(status=3)
    if request.POST:
        keyword = request.POST.get("search")
        if keyword:
            all_patients = []
            for p in UserProfile.objects.all():
                if keyword in UserProfile.get_full_name(p):
                    all_patients.append(p)
                    num_patients += 1

    return render(request, 'view_all_patients.html', {'all_patients': all_patients,
                                                      'keyword': keyword,
                                                      'num_patients': num_patients})


@login_required
def view_patient(request, patient_id):
    patient = UserProfile.objects.get(pk=patient_id)
    user = patient.user

    return render(request, 'view_patient.html', {'the_patient': patient, 'the_user': user})


@login_required
def admit_patient(request):
    if request.POST:
        post = request.POST

        doctor = None
        nurse = None

        if request.user.userprofile.is_doctor():
            nurse = UserProfile.objects.get(id=post.get("nurse"))
            doctor = UserProfile.objects.get(id=request.user.userprofile.id)

        elif request.user.userprofile.is_nurse():
            nurse = UserProfile.objects.get(id=request.user.userprofile.id)
            doctor = UserProfile.object.get(id=post.get("doctor"))

        patient = UserProfile.objects.get(id=post.get("patient"))
        hospital = Hospital.objects.get(hospital_id=post.get("hospital"))

        saved = HospitalStay.objects.create(patient=patient, hospital=hospital,
                                            doctor=doctor, nurse=nurse)

        if saved:
            return redirect('admit_patient')

    patients = UserProfile.objects.filter(status=3)
    nurses = UserProfile.objects.filter(status=2)
    doctors = UserProfile.objects.filter(status=1)

    your_stays = HospitalStay.objects.filter(nurse=request.user.userprofile, discharge__isnull=True) | \
                 HospitalStay.objects.filter(doctor=request.user.userprofile, discharge__isnull=True)

    archives = HospitalStay.objects.filter(discharge__isnull=False)
    hospital = HospitalStaff.objects.filter(user_profile=request.user.userprofile)
    all_stays = HospitalStay.objects.filter(discharge__isnull=True,
                                            hospital__in=hospital.filter(user_profile=request.user.userprofile)
                                            .values_list('hospital_id', flat=True))

    return render(request, 'admit_patient.html', {'patients': patients, 'all_stays': all_stays,
                                                  'your_stays': your_stays, 'hospitals': hospital,
                                                  'nurses': nurses, 'doctors': doctors,
                                                  'archives': archives})


def discharge_patient(request, id):
    if request.POST:
        HospitalStay.objects.filter(id=id).update(discharge=timezone.now())

    return redirect('admit_patient')


def edit_patient_medical_info(request, patient_id):
    patient = User.objects.get(pk=patient_id)
    patient_up = UserProfile.objects.get(pk=patient_id)
    patient_mi = MedicalInformation.objects.get(user=patient_up)

    if request.POST:
        post = request.POST
        patient_mi.height = float(post.get("height"))
        patient_mi.weight = float(post.get("weight"))
        patient_mi.sex = post.get("sex")
        patient_mi.medications = post.get("medications")
        patient_mi.allergies = post.get("allergies")
        patient_mi.medical_conditions = post.get("medical_conditions")
        patient_mi.family_history = post.get("family_history")
        patient_mi.additional_info = post.get("additional_info")
        patient_mi.primary_hospital = Hospital.objects.get(pk=post.get("primary_hospital"))
        patient_mi.save()

        return redirect('view_patient', patient_id=patient.pk)

    hospitals = Hospital.objects.all()
    return render(request, 'edit_patient_medical_info.html', {'the_patient': patient,
                                                              'hospitals': hospitals,
                                                              'patient_up': patient_up,
                                                              'patient_mi': patient_mi})


def patient_transfer(request, id=None):
    if request.POST and id is not None:
        post = request.POST
        patient = UserProfile.objects.get(pk=post.get("patient_id"))
        from_hospital = Hospital.objects.get(pk=post.get("transfer_from"))
        to_hospital = Hospital.objects.get(pk=post.get("transfer_to"))

        Transfers.objects.create(transfer_patient=patient,
                                 from_hospital=from_hospital,
                                 to_hospital=to_hospital,
                                 date_accepted=timezone.now(),
                                 receiver=request.user.userprofile)

        HospitalStay.objects.filter(id=id).update(hospital=to_hospital)

        return redirect('patient_transfer')

    your_hospitals = HospitalStaff.objects.filter(user_profile=request.user.userprofile)
    all_stays = HospitalStay.objects.exclude(hospital__in=your_hospitals.values_list('hospital_id', flat=True))

    return render(request, 'patient_transfer.html', {'all_stays': all_stays, 'your_hospitals': your_hospitals})


def prescriptions(request):
    if request.POST:
        post = request.POST
        patient = MedicalInformation.objects.get(pk=post.get("patient"))
        name = post.get("name")
        description = post.get("description")
        notes = post.get("notes")
        instructions = post.get("instructions")
        dosage = post.get("dosage")
        Prescription.objects.create(doctor=request.user,
                                    patient=patient.user,
                                    name=name,
                                    description=description,
                                    notes=notes,
                                    instructions=instructions,
                                    dosage=dosage)

    all_prescriptions = None
    your_prescriptions = None
    your_hospitals = None

    if request.user.userprofile.is_doctor():
        all_prescriptions = Prescription.objects.all()
        your_prescriptions = Prescription.objects.filter(doctor=request.user)
        html = 'doc_prescriptions.html'

    if request.user.userprofile.is_nurse():
        your_hospitals = HospitalStaff.objects.filter(user_profile=request.user.userprofile).values_list('hospital_id',
                                                                                                         flat=True)
        your_prescriptions = Prescription.objects.filter(Q(__startswith='What'))
        html = 'nur_prescriptions.html'

    patients = MedicalInformation.objects.all()

    return render(request, html, {'prescriptions': all_prescriptions,
                                  'your_prescriptions': your_prescriptions,
                                  'patients': patients})


def export_data(request):
    user_profile = UserProfile.objects.get(pk=request.user.userprofile.id).get_csv()
    medical_info = MedicalInformation.objects.get(user=request.user.userprofile.medicalinformation.id).get_csv()
    prescriptions = Prescription.objects.filter(patient=request.user.userprofile.id)
    insurance = Insurance.objects.filter(medical_information=request.user.userprofile.medicalinformation.id)
    emergency_contact = EmergencyContact.objects.filter(pk=request.user.userprofile.medicalinformation.id)
    hospital_stay = HospitalStay.objects.filter(patient=request.user.userprofile.id)
    appointment = Appointment.objects.filter(patient=request.user.userprofile.id)

    data = "{},{},{},{}".format(request.user.first_name, request.user.last_name, request.user.email,
                                request.user.username, request.user.password)

    data += "Profile:{}\nMedical-Info:{}\n".format(user_profile, medical_info)

    for v in prescriptions:
        data += "Prescription:{}\n".format(v.get_csv())

    for v in insurance:
        data += "Insurance:{}\n".format(v.get_csv())

    for v in emergency_contact:
        data += "Emergency-Contact:{}\n".format(v.get_csv())

    for v in hospital_stay:
        data += "Hospital-Stay:{}\n".format(v.get_csv())

    for v in appointment:
        data += "Appointment:{}\n".format(v.get_csv())

    response = HttpResponse(data, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="{}_{}.txt"'.format(request.user.userprofile
                                                                                .get_full_name(),
                                                                                timezone.now())

    return response


def system_statistics(request):
    your_hospitals = HospitalStaff.objects.filter(user_profile=request.user.userprofile)
    patients = UserProfile.objects.filter(status=3)

    num_patients_in_hospital = HospitalStay.objects.filter(
        hospital__in=your_hospitals.values_list('hospital_id', flat=True),
        discharge__isnull=False).count()

    avg_num_visits = int(HospitalStay.objects.filter(hospital__in=your_hospitals.values_list('hospital_id', flat=True)) \
                         .count() / UserProfile.objects.filter(status=3).count())

    times = HospitalStay.objects.filter(hospital__in=your_hospitals.values_list('hospital_id', flat=True),
                                        discharge__isnull=False, patient__in=patients.values_list('id', flat=True))

    avg_time = 0
    total_times = 0

    for time in times:
        total_times += 1
        avg_time += ((time.discharge - time.admission).total_seconds() / 60)

    avg_time = round(avg_time / total_times, 2)
    patients_receiving_prescriptions = Prescription.objects.values('patient').annotate(Count('patient')).order_by()

    return render(request, "system_statistics.html", {'num_patients_in_hospital': num_patients_in_hospital,
                                                      'avg_num_visits': avg_num_visits,
                                                      'avg_time': avg_time,
                                                      'patients_receiving_prescriptions': patients_receiving_prescriptions.count()
                                                      })


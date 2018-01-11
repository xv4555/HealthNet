from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User


class UserStatus(models.Model):
    """
    This is the class that holds our information for the type of a user a user is.
    We have Doctor, Admin, Patient, Nurse
    """
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return "{0}".format(self.status_name)


class Hospital(models.Model):
    """
    This holds information the Hospital model
    """
    hospital_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)

    def __str__(self):
        return "Hospital: {0}, Address: {1}, City: {2}, State: {3}, Zip: {4}".format(self.name, self.address, self.city,
                                                                                     self.state, self.zipcode)


class UserProfile(models.Model):
    """
    This adds more functionality to the user class without having to extend it fully,
    build a new authentication system. Doing this we added more inforamtion that didn't come
    out the box with the django authentication library.
    """
    user = models.OneToOneField(
                                  User,
                                  null=True,
                                  on_delete=models.CASCADE,
                                  )
                                  #user = models.OneToOneField(User, null=True)
    phone_number = models.CharField(max_length=30)
    status = models.ForeignKey(UserStatus, null=True, on_delete=models.CASCADE)
    primary_hospital = models.ForeignKey(Hospital, null=True, blank=True,on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['phone_number']

    def get_csv(self):
        return "{},{},{},{}".format(
            self.get_full_name(),
            self.phone_number,
            self.status.status_name,
            self.primary_hospital.name)

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)

    # These are helper functions for us to use when we need to check on the type of users.
    def is_admin(self):
        return self.status.status_id is 4

    def is_doctor(self):
        return self.status.status_id is 1

    def is_nurse(self):
        return self.status.status_id is 2

    def is_patient(self):
        return self.status.status_id is 3

    def get_appointments(self):
        """
        Gets all appointments based on the type of user the user is.
        """
        if self.is_admin():
            return Appointment.objects

        elif self.is_doctor():
            return Appointment.objects.filter(doctor=self)

        return Appointment.objects.filter(patient=self)

    def get_full_name(self):
        """
        Gets the full name of the patient
        """
        return "{0} {1}".format(self.user.first_name, self.user.last_name)


class MedicalInformation(models.Model):
    """
    This method would build the medical information out so that
    we can store information on the medical system.
    """
    user = models.OneToOneField(UserProfile, null=True, on_delete=models.CASCADE)
    sex = models.CharField(max_length=50)
    medications = models.CharField(max_length=400, null=True)
    allergies = models.CharField(max_length=400, null=True)
    medical_conditions = models.CharField(max_length=400, null=True)
    family_history = models.CharField(max_length=400, null=True)
    additional_info = models.CharField(max_length=600, null=True)
    height = models.CharField(max_length=5)
    weight = models.CharField(max_length=5)

    def get_csv(self):
        return "{},{},{},{},{},{},{}".format(
            self.user.get_full_name(),
            self.sex,
            self.medications,
            self.allergies,
            self.medical_conditions,
            self.family_history,
            self.additional_info
        )

    def __str__(self):
        return ("Name: {6} Sex: {0}, Medications: {1}, Allergies: {2}, " +
                "Medical Conditions: {3}, Family History: {4}," +
                " Additional Info: {5}").format(
            self.sex, self.medications,
            self.allergies, self.medical_conditions,
            self.family_history, self.additional_info, self.user.get_full_name()
        )


class Prescription(models.Model):
    """
    This holds prescription information
    """
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField()
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()

    def __str__(self):
        return 'Doctor: {0}, Prescription: {1}, Dosage: {2}'.format(self.doctor.get_full_name(),
                                                                    self.name,
                                                                    self.dosage)

    def get_csv(self):
        return "{},{},{},{},{},{},{}".format(
            self.patient.get_full_name(),
            self.patient.get_full_name(),
            self.name,
            self.description,
            self.notes,
            self.dosage,
            self.instructions
        )


class Insurance(models.Model):
    """
    This adds an insurance provider model the user profile.
    """
    medical_information = models.ForeignKey(MedicalInformation, null=True, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=200)
    company = models.CharField(max_length=200)

    def __str__(self):
        return "{0} with {1}".format(self.policy_number, self.company)

    def get_csv(self):
        return "{},{},{}".format(
            self.medical_information,
            self.policy_number,
            self.company
        )


class HospitalStaff(models.Model):
    """"
    This holds information on who works at a specific hospital
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def get_csv(self):
        return "{},{}".format(
            self.user_profile.get_full_name(),
            self.hospital.name
        )

    def __str__(self):
        return "First: {0}, Last: {1}, Hospital: {2}, Status: {3}".format(
            self.user_profile.user.first_name, self.user_profile.user.last_name,
            self.hospital.name, self.user_profile.status.status_name,
        )


class EmergencyContact(models.Model):
    """
    This holds information that the user can use to talk about his or her
    """
    user_profile_id = models.ForeignKey(MedicalInformation, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=30)
    relationship = models.CharField(max_length=30)

    def get_csv(self):
        return "{},{},{},{}".format(
            self.first_name,
            self.last_name,
            self.phone_number,
            self.relationship
        )

    def __str__(self):
        return "First: {0}, Last: {1}, Phone: {2}, Relationships: {3}".format(
            self.first_name, self.last_name, self.phone_number,
            self.relationship,
        )


class Message(models.Model):
    """This holds information about the messages sent between users."""
    user_from = models.ForeignKey(UserProfile, related_name='user_from', null=True, on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserProfile, related_name='user_to', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    read = models.SmallIntegerField()

    def __str__(self):
        return "From: {0} To: {1}, {2} {3} {4}".format(self.user_from, self.user_to,
                                                       self.time, self.subject, self.message)


class HospitalStay(models.Model):
    """
    This will hold the user in the hospital for x amount of days.
    """
    patient = models.ForeignKey(UserProfile, related_name="patient", on_delete=models.CASCADE)
    admission = models.DateTimeField(auto_now_add=True)
    discharge = models.DateTimeField(null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserProfile, related_name="referring_doctor", null=True, on_delete=models.CASCADE)
    nurse = models.ForeignKey(UserProfile, related_name="referring_nurse", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} {1} {2}".format(self.patient.user.first_name, self.admission, self.discharge)

    def get_csv(self):
        return "{},{},{},{},{},{}".format(
            self.patient.get_full_name(),
            self.admission,
            self.discharge,
            self.hospital.name,
            self.doctor.get_full_name(),
            self.nurse.get_full_name()
        )


class Transfers(models.Model):
    """
    This will hold the patient transfer information
    """
    transfer_patient = models.ForeignKey(UserProfile, related_name="transfer_patient", on_delete=models.CASCADE)
    from_hospital = models.ForeignKey(Hospital, related_name="from_hospital", on_delete=models.CASCADE)
    to_hospital = models.ForeignKey(Hospital, related_name="to_hospital", on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name="receiver", null=True, blank=True, on_delete=models.CASCADE)
    date_accepted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Patient: {0}, From: {1}, To: {2}, Sender: {3}, Receiver: {4}, Status: {5}". \
            format(self.transfer_patient.get_full_name(), self.from_hospital.name,
                   self.to_hospital.name, self.sender.get_full_name(), self.sender.get_full_name(),
                   self.status)


class Appointment(models.Model):
    """
    This holds the appointment data for a user.
    """
    patient = models.ForeignKey(User, related_name='patient_appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor_appointments', on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    def get_csv(self):
        return "{},{},{},{}".format(
            self.patient.get_full_name(),
            self.doctor.get_full_name(),
            self.notes,
            self.date.isoformat()
        )

    def __str__(self):
        return '{0} - {1} Seeing: {2}'.format(self.date.strftime('%m/%d/%Y'), self.patient,
                                              self.doctor)

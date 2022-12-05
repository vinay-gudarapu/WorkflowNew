from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
class Employee(AbstractUser):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobileoffice = models.CharField(max_length=15, null=True)
    mobilepersonal = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=50, null=True, unique=True)
    departmentid = models.IntegerField(null=True)
    addressline1 = models.CharField(max_length=100, null=True)
    addressline2 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=20, null=True)
    enablelogin = models.CharField(max_length=1, null=True)
    type = models.CharField(max_length=10, null=True)
    picture = models.BinaryField(null=True)
    status = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'employee'


# Function for create the token for each user
@receiver(post_save, sender=Employee)
def create_auth_token_for_user(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'department'


class Holiday(models.Model):
    id = models.AutoField(primary_key=True)
    holidaydate = models.DateTimeField()
    holidaypurpose = models.CharField(max_length=100, null=True)
    holidayname = models.CharField(max_length=100, null=True)
    holidaytype = models.CharField(max_length=1)
    status = models.CharField(max_length=1)

    class Meta:
        db_table = 'holiday'


class HolidayDepartment(models.Model):
    id = models.AutoField(primary_key=True)
    holidayid = models.IntegerField()
    departmentid = models.IntegerField()

    class Meta:
        db_table = 'holidaydepartment'


class HolidayLocation(models.Model):
    id = models.AutoField(primary_key=True)
    holidayid = models.IntegerField()
    holidaylocation = models.CharField(max_length=100)

    class Meta:
        db_table = 'holidaylocation'


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)
    departmentid = models.IntegerField()
    teamlead = models.IntegerField()
    status = models.CharField(max_length=1)

    class Meta:
        db_table = 'team'


class TeamMember(models.Model):
    id = models.AutoField(primary_key=True)
    teamid = models.IntegerField()
    employeeid = models.IntegerField()

    class Meta:
        db_table = 'teammember'


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    period = models.IntegerField()
    tax = models.DecimalField(max_digits=5, decimal_places=3)
    status = models.CharField(max_length=1)

    class Meta:
        db_table = 'service'


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    taskname = models.CharField(max_length=100)
    serviceid = models.IntegerField(null=True)
    propertytypeid = models.IntegerField(null=True)
    status = models.CharField(max_length=1)
    dependenttaskid = models.IntegerField(null=True)

    class Meta:
        db_table = 'task'


class PropertyType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    iconurl = models.CharField(max_length=126)

    class Meta:
        db_table = 'propertytype'


class TaskActivity(models.Model):
    id = models.AutoField(primary_key=True)
    activityname = models.CharField(max_length=100)
    departmentid = models.IntegerField(null=True)
    taskid = models.IntegerField(null=True)
    effortsorginal = models.IntegerField(null=True)
    effortsactual = models.IntegerField(null=True)
    timelineorgnial = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    timelineactual = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    documents = models.CharField(max_length=100, null=True)
    taskactivitycol = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'taskactivity'


class RequestTask(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.IntegerField(null=True)
    taskid = models.IntegerField(null=True)

    class Meta:
        db_table = 'requesttask'


class RequestDB(models.Model):
    id = models.AutoField(primary_key=True)
    serviceid = models.IntegerField()
    requestername = models.CharField(max_length=100)
    requestermobilestatus = models.CharField(max_length=1, null=True)
    requesteremail = models.CharField(max_length=100, null=True)
    requestermobile = models.CharField(max_length=100, null=True)
    requesteremailstatus = models.CharField(max_length=1, null=True)
    requesteraddressline1 = models.CharField(max_length=100, null=True)
    requesteraddressline2 = models.CharField(max_length=100, null=True)
    requestercity = models.CharField(max_length=100, null=True)
    requesterstate = models.CharField(max_length=100, null=True)
    requestercountry = models.CharField(max_length=100, null=True)
    requesterpin = models.CharField(max_length=10, null=True)
    requesteridentitytype = models.CharField(max_length=1, null=True)
    requesteridentitynumber = models.CharField(max_length=45, null=True)
    agentcode = models.CharField(max_length=15, null=True)
    requeststatus = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'requestdb'


class RequestProperty(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.IntegerField(null=True)
    ispropertylisted = models.CharField(max_length=1)
    propertylocation = models.CharField(max_length=100, null=True)
    propertyrevenuevillage = models.CharField(max_length=100, null=True)
    propertymandal = models.CharField(max_length=100, null=True)
    propertydistrict = models.CharField(max_length=100, null=True)
    propertytype = models.CharField(max_length=1, null=True)
    layoutapprovedby = models.CharField(max_length=20, null=True)
    approvalnumber = models.CharField(max_length=50, null=True)
    locationgeotag = models.CharField(max_length=100, null=True)
    latestsaledeedno = models.CharField(max_length=100, null=True)
    latestsaledeedyear = models.IntegerField(null=True)
    latestsaledeedsro = models.CharField(max_length=100, null=True)
    venturename = models.CharField(max_length=100, null=True)
    houseno = models.CharField(max_length=100, null=True)
    wardorblocknumber = models.CharField(max_length=40, null=True)
    areaname = models.CharField(max_length=100, null=True)
    phase = models.CharField(max_length=40, null=True)
    plotarea = models.DecimalField(max_digits=13, decimal_places=2, null=True)
    constructedarea = models.DecimalField(max_digits=13, decimal_places=2, null=True)
    plintharea = models.DecimalField(max_digits=13, decimal_places=2, null=True)
    ispattedharinposession = models.CharField(max_length=1, null=True)
    reasonfornotinposession = models.CharField(max_length=200, null=True)
    ptinnumber = models.CharField(max_length=40, null=True)
    anypreexistinglitigations = models.CharField(max_length=1, null=True)
    buildingpermissionnumber = models.CharField(max_length=40, null=True)
    layoutpermissionnumber = models.CharField(max_length=40, null=True)
    buildingapprovaldoc = models.BinaryField(null=True)
    layoutapprovaldoc = models.BinaryField(null=True)
    extentin = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'requestproperty'


class Preliminary(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.IntegerField()
    startdate = models.DateTimeField(null=True)
    donedate = models.DateTimeField(null=True)
    status = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'preliminary'


class PreliminaryTask(models.Model):
    id = models.AutoField(primary_key=True)
    tasktype = models.CharField(max_length=1, null=True)
    prelimid = models.IntegerField(null=True)
    requestid = models.IntegerField(null=True)
    assignedto = models.IntegerField(null=True)
    verifiedby = models.IntegerField(null=True)
    assigneddate = models.DateTimeField(null=True)
    completeddate = models.DateTimeField(null=True)
    status = models.CharField(max_length=1, null=True)
    notes = models.CharField(max_length=512, null=True)
    remarks = models.CharField(max_length=512, null=True)
    entryhours = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    verifyhours = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    verifystatus = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'preliminarytask'


class Dharani(models.Model):
    id = models.AutoField(primary_key=True)
    prelimtaskid = models.IntegerField()
    requestid = models.IntegerField()
    sno = models.IntegerField()
    district = models.CharField(max_length=100, null=True)
    mandal = models.CharField(max_length=100, null=True)
    village = models.CharField(max_length=100, null=True)
    surveyno = models.CharField(max_length=100, null=True)
    extent = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    pattadharname = models.CharField(max_length=100, null=True)
    isdigitallysigned = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'dharani'


class ProhibitedLand(models.Model):
    id = models.AutoField(primary_key=True)
    prelimtaskid = models.IntegerField()
    requestid = models.IntegerField()
    sno = models.IntegerField()
    village = models.CharField(max_length=100, null=True)
    surveyno = models.CharField(max_length=100, null=True)
    extent = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    pattadharname = models.CharField(max_length=100, null=True)
    natureofland = models.CharField(max_length=100, null=True)
    landclassification = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'prohibitedland'


class Encumbrance(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.IntegerField()
    sno = models.IntegerField()
    reqdocno = models.CharField(max_length=50, null=True)
    doctype = models.CharField(max_length=40, null=True)
    claimantname = models.CharField(max_length=100, null=True)
    executantname = models.CharField(max_length=100, null=True)
    surveyno = models.CharField(max_length=40, null=True)
    extent = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    village = models.CharField(max_length=50, null=True)
    mandal = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'encumbrance'


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.IntegerField()
    task = models.CharField(max_length=1)
    filename = models.CharField(max_length=100)
    filetype = models.CharField(max_length=1)
    filecontent = models.BinaryField(null=True)

    class Meta:
        db_table = 'document'


class Checklist(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.CharField(max_length=1)
    question = models.CharField(max_length=512, null=True)
    choice = models.CharField(max_length=40, null=True)
    yestask = models.CharField(max_length=1, null=True)
    notask = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'checklist'


class Checklistanswer(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.IntegerField()
    task = models.CharField(max_length=1)
    question = models.CharField(max_length=512, null=True)
    choice = models.CharField(max_length=40, null=True)
    answer = models.CharField(max_length=40, null=True)

    class Meta:
        db_table = 'checklistanswer'


class Urbanland(models.Model):
    id = models.AutoField(primary_key=True)
    qid = models.IntegerField()
    requestid = models.IntegerField()
    response = models.CharField(max_length=512, null=True)
    prelimurbancol = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'urbanland'


class LegalCase(models.Model):
    id = models.AutoField(primary_key=True)
    requestid = models.IntegerField()
    sno = models.IntegerField()
    casenumber = models.CharField(max_length=40, null=True)
    courtname = models.CharField(max_length=100, null=True)
    petitioners = models.CharField(max_length=256, null=True)
    defendants = models.CharField(max_length=256, null=True)
    casestatus = models.CharField(max_length=1, null=True)
    ordernumber = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'legalcase'

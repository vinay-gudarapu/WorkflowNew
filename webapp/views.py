import base64

from allauth.account.utils import perform_login
from django.contrib import messages
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import render, redirect

# Create your views here.
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from workflowapp.models import Holiday, HolidayDepartment, Employee, Team, HolidayLocation, TeamMember, Department, \
    Task, Service, PropertyType, TaskActivity, RequestDB, RequestProperty, PreliminaryTask, Dharani, ProhibitedLand, \
    Encumbrance, LegalCase, Checklist, Checklistanswer, Urbanland
from allauth.account import app_settings as allauth_settings


@api_view(['GET', 'POST'])
def login(request):
    try:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            employee = Employee.objects.filter(email=email).first()
            if not employee:
                messages.warning(request, 'User Not Found')
                raise Exception
            verification = pbkdf2_sha256.verify(password, employee.password)
            if not verification:
                messages.warning(request, 'Invalid password')
                raise Exception
            perform_login(request._request, employee, allauth_settings.EMAIL_VERIFICATION, signup=False,
                          redirect_url=None, signal_kwargs=None)
            return redirect('holidays')
        else:
            return render(request, "login.html")
    except Exception as e:
        print(str(e))
        return render(request, "login.html")


def holidays(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        holidays = Holiday.objects.all()
        holidays_list = []
        for holiday in holidays:
            department = HolidayDepartment.objects.filter(holidayid=holiday.id).values_list('departmentid', flat=True)
            departments = Department.objects.filter(id__in=list(department)).values_list('name', flat=True)
            holidays_list.append(
                {'date': holiday.holidaydate.date(), 'name': holiday.holidayname,
                 'type': "Mandatory" if holiday.holidaytype == 'M' else 'Optional',
                 'department': ",".join(list(departments)), 'status': 'Active' if holiday.status == "A" else 'Inactive',
                 'id': holiday.id})
        return render(request, "sidebar.html", {"template_name": "holidaylist.html", "holidays_list": holidays_list})
    except Exception as e:
        print(str(e))
        return redirect('holidays')


def add_holiday(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        if request.method == "POST":
            dataObj = request.POST
            print(dataObj)
            name = dataObj['name']
            date = dataObj['date']
            holiday_type = dataObj['type']
            departments = request.POST.getlist('departments')
            print(departments)
            states = request.POST.getlist('state')
            print(states)
            status = dataObj['status']
            hldy = Holiday.objects.create(holidaydate=date, holidayname=name, holidaytype=holiday_type,
                                          status=status)
            for department in departments:
                HolidayDepartment.objects.create(holidayid=hldy.id, departmentid=department)
            for state in states:
                HolidayLocation.objects.create(holidayid=hldy.id, holidaylocation=state)
            messages.success(request, 'Holiday added successfully')
            return redirect('holidays')
        else:
            departments = Department.objects.all().values('id', 'name')
            return render(request, "sidebar.html",
                          {"template_name": "addholiday.html", "departments": list(departments)})
    except Exception as e:
        print(str(e))
        return redirect('holidays')


def edit_holiday(request, hldy_id):
    try:
        if not request.user.is_active:
            return redirect('login')
        if request.method == "POST":
            dataObj = request.POST
            name = dataObj['name']
            date = dataObj['date']
            holiday_type = dataObj['type']
            departments = request.POST.getlist('departments')
            states = request.POST.getlist('state')
            status = dataObj['status']
            Holiday.objects.filter(id=hldy_id).update(holidaydate=date, holidayname=name, holidaytype=holiday_type,
                                                      status=status)
            HolidayDepartment.objects.filter(holidayid=hldy_id).delete()
            HolidayLocation.objects.filter(holidayid=hldy_id).delete()
            for department in departments:
                HolidayDepartment.objects.create(holidayid=hldy_id, departmentid=department)
            for state in states:
                HolidayLocation.objects.create(holidayid=hldy_id, holidaylocation=state)
            messages.success(request, 'Holiday edited successfully')
            return redirect('holidays')
        else:
            departments = Department.objects.all().values('id', 'name')
            holiday = Holiday.objects.get(id=hldy_id)
            name = holiday.holidayname
            holidaydate = str(holiday.holidaydate.date())
            holidaytype = holiday.holidaytype
            status = holiday.status
            hldy_deps = HolidayDepartment.objects.filter(holidayid=hldy_id).values_list('departmentid', flat=True)
            hldy_locs = HolidayLocation.objects.filter(holidayid=hldy_id).values_list('holidaylocation', flat=True)
            return render(request, "sidebar.html",
                          {"template_name": "edit_holiday.html", "departments": list(departments),
                           "name": name, "holidaydate": holidaydate, 'holidaytype': holidaytype, 'status': status,
                           "hldy_deps": list(hldy_deps), 'hldy_locs': hldy_locs})
    except Exception as e:
        print(str(e))
        return redirect('holidays')


def add_employee(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        if request.method == "POST":
            dataObj = request.POST
            file = request.FILES
            firstname = dataObj['firstname']
            lastname = dataObj['lastname']
            emp_type = dataObj['type']
            department = dataObj['department']
            mob_official = dataObj['mob_official']
            mob_personal = dataObj['mob_personal']
            email = dataObj['email']
            address_line1 = dataObj['address_line1']
            address_line2 = dataObj['address_line2']
            city = dataObj['city']
            state = dataObj['state']
            country = dataObj['country']
            pincode = dataObj['pincode']
            password = pbkdf2_sha256.encrypt(dataObj['password'])
            status = dataObj['status']
            picture = file.get('profile', None).read() if file.get('profile', None) else None
            Employee.objects.create(firstname=firstname, lastname=lastname, type=emp_type, departmentid=department,
                                    mobileoffice=mob_official, mobilepersonal=mob_personal, email=email, username=email,
                                    addressline1=address_line1, addressline2=address_line2, city=city, state=state,
                                    country=country, pincode=pincode, password=password, status=status,
                                    picture=picture)
            messages.success(request, 'Employee added successfully')
            return redirect('employees')
        else:
            departments = Department.objects.all().values('id', 'name')
            return render(request, "sidebar.html",
                          {"template_name": "addemployee.html", "departments": list(departments)})
    except Exception as e:
        print(str(e))
        return redirect('employees')


def edit_employee(request, emp_id):
    try:
        if not request.user.is_active:
            return redirect('login')
        if request.method == "POST":
            dataObj = request.POST
            file = request.FILES
            firstname = dataObj['firstname']
            lastname = dataObj['lastname']
            emp_type = dataObj['type']
            department = dataObj['department']
            mob_official = dataObj['mob_official']
            mob_personal = dataObj['mob_personal']
            email = dataObj['email']
            address_line1 = dataObj['address_line1']
            address_line2 = dataObj['address_line2']
            city = dataObj['city']
            state = dataObj['state']
            country = dataObj['country']
            pincode = dataObj['pincode']
            password = pbkdf2_sha256.encrypt(dataObj['password'])
            status = dataObj['status']
            picture = file.get('profile', None).read() if file.get('profile', None) else None
            employee = Employee.objects.filter(id=emp_id)
            employee.update(firstname=firstname, lastname=lastname, type=emp_type, email=email, departmentid=department,
                            mobileoffice=mob_official, username=email, mobilepersonal=mob_personal,
                            addressline1=address_line1, addressline2=address_line2, city=city, state=state,
                            country=country, pincode=pincode, password=password, status=status)
            if picture:
                employee.first().picture = picture
                employee.first().save()
            messages.success(request, 'Employee edited successfully')
            return redirect('employees')
        else:
            departments = Department.objects.all().values('id', 'name')
            employee = Employee.objects.filter(id=emp_id).values().first()
            image = base64.b64encode(employee['picture']).decode() if employee['picture'] else None
            return render(request, "sidebar.html",
                          {"template_name": "edit_employee.html", "departments": list(departments),
                           "employee": employee, 'image': image})
    except Exception as e:
        print(str(e))
        return redirect('employees')


def employees(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        emp_list = []
        for emp in Employee.objects.all():
            department = Department.objects.get(id=emp.departmentid)
            obj = {'name': f'{emp.firstname} {emp.lastname}', 'mobile': emp.mobileoffice, 'dep': department.name,
                   'loc': emp.city, 'status': 'Active' if emp.status == 'A' else 'Inactive', 'id': emp.id}
            emp_list.append(obj)
        return render(request, "sidebar.html", {"template_name": "employeelist.html", "emp_list": emp_list})
    except Exception as e:
        print(str(e))
        return redirect('employees')


def add_team(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        if request.method == "POST":
            dataObj = request.POST
            print(dataObj)
            name = dataObj['name']
            teamlead = dataObj['team_lead']
            members = dataObj.getlist('members')
            department = dataObj['department']
            location = dataObj['location']
            status = dataObj['status']
            new_team = Team.objects.create(teamname=name, location=location, departmentid=department, teamlead=teamlead,
                                           status=status)
            for memb in members:
                TeamMember.objects.create(teamid=new_team.id, employeeid=memb)
            messages.success(request, 'New Team Created successfully')
            return redirect('teams')
        else:
            departments = Department.objects.all().values('id', 'name')
            employees_list = Employee.objects.all().values('id', 'firstname', 'lastname', 'picture')
            print(employees_list.last())
            return render(request, "sidebar.html",
                          {"template_name": "addteam.html", "departments": list(departments),
                           'employees_list': list(employees_list)})
    except Exception as e:
        print(str(e))
        return redirect('teams')


def edit_team(request, team_id):
    try:
        if not request.user.is_active:
            return redirect('login')
        if request.method == "POST":
            dataObj = request.POST
            print(dataObj)
            name = dataObj['name']
            teamlead = dataObj['team_lead']
            members = dataObj.getlist('members')
            department = dataObj['department']
            location = dataObj['location']
            status = dataObj['status']
            Team.objects.filter(id=team_id).update(teamname=name, location=location, departmentid=department,
                                                   teamlead=teamlead, status=status)
            TeamMember.objects.filter(id=team_id).delete()
            for memb in members:
                TeamMember.objects.create(teamid=team_id, employeeid=memb)
            messages.success(request, 'Team edited successfully')
            return redirect('teams')
        else:
            departments = Department.objects.all().values('id', 'name')
            employees_list = Employee.objects.all().values('id', 'firstname', 'lastname', 'picture')
            team = Team.objects.filter(id=team_id).values().first()
            team_list = TeamMember.objects.filter(teamid=team_id).values_list('employeeid', flat=True)
            return render(request, "sidebar.html",
                          {"template_name": "editteam.html", "departments": list(departments),
                           'employees_list': list(employees_list), 'team': team, 'team_list': list(team_list)})
    except Exception as e:
        print(str(e))
        return redirect('teams')


def teams(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        teams_list = []
        for team in Team.objects.all():
            employee = Employee.objects.get(id=team.teamlead)
            department = Department.objects.get(id=team.departmentid)
            obj = {'name': team.teamname, 'location': team.location, 'id': team.id,
                   'team_lead': f'{employee.firstname} {employee.lastname}',
                   'dep': department.name, 'status': 'Active' if team.status == 'A' else 'Inactive'}
            teams_list.append(obj)
        return render(request, "sidebar.html", {"template_name": "teamslist.html", "teams_list": teams_list})
    except Exception as e:
        print(str(e))
        return redirect('teams')


def tasks(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        tasks_list = []
        for task in Task.objects.all():
            service = Service.objects.get(id=task.serviceid)
            propertytype = PropertyType.objects.get(id=task.propertytypeid)
            activities = TaskActivity.objects.filter(taskid=task.id).values_list('activityname', flat=True)
            obj = {'name': task.taskname, 'service': service.name,
                   'property_type': propertytype.description,
                   'activities': activities.count(),
                   'status': 'Active' if task.status == 'A' else 'Inactive'}
            tasks_list.append(obj)
        return render(request, "sidebar.html", {"template_name": "tasks.html", "tasks_list": tasks_list})
    except Exception as e:
        print(str(e))
        return redirect('tasks')


def add_tasks(request):
    try:
        if not request.user.is_active:
            return redirect('login')
        if request.method == "POST":
            dataObj = request.POST
            name = dataObj['name']
            serviceid = dataObj['service_type']
            propertytypeid = dataObj['propertytypeid']
            status = dataObj['status']
            dependenttaskid = dataObj.get('dependenttaskid', None)
            task = Task.objects.create(taskname=name, serviceid=serviceid, propertytypeid=propertytypeid,
                                       status=status, dependenttaskid=dependenttaskid)
            for activity in dataObj['activities']:
                activityname = activity['activityname']
                departmentid = activity['departmentid']
                effortsorginal = activity['effortsorginal']
                timelineorgnial = activity['timelineorgnial']
                documents = activity['documents']
                taskactivitycol = activity['taskactivitycol']
                TaskActivity.objects.create(activityname=activityname, departmentid=departmentid, taskid=task.id,
                                            effortsorginal=effortsorginal, effortsactual=0, timelineactual=0,
                                            timelineorgnial=timelineorgnial, documents=documents,
                                            taskactivitycol=taskactivitycol)
            messages.success(request, 'New Task Created successfully')
            return redirect('tasks')
        else:
            departments = Department.objects.all().values('id', 'name')
            services_list = Service.objects.all().values('id', 'name')
            dependent_task = Task.objects.all().values('id', 'taskname')
            return render(request, "sidebar.html",
                          {"template_name": "addtasks.html", "departments": list(departments),
                           'services_list': list(services_list), 'dependent_task': list(dependent_task)})
    except Exception as e:
        print(str(e))
        return redirect('tasks')


def getdetails(data):
    status = data.verifystatus
    assigned = data.assignedto
    verified = data.verifiedby
    if not status or status == 'P':
        status = "Pending"
        color = "#0000AF"
    elif status == 'I':
        status = "In Progress"
        color = "#FFA500"
    else:
        status = "Completed"
        color = "#228B22"
    if assigned:
        employee = Employee.objects.get(id=assigned)
        assigned_name = f'{employee.firstname} {employee.lastname}'

    else:
        assigned_name = 'N/A'
    assigned_id = assigned
    if verified:
        employee = Employee.objects.get(id=verified)
        verified_name = f'{employee.firstname} {employee.lastname}'
    else:
        verified_name = 'N/A'
    verified_id = verified
    return {"status": status, "assigned_name": assigned_name, "verified_name": verified_name,
            "assigned_on": data.assigneddate if data.assigneddate else 'N/A',
            "completeddate": data.completeddate if data.completeddate else 'N/A', "color": color,
            "verified_id": verified_id, "assigned_id": assigned_id, 'task_id': data.id}


def preliminary_verification(request, req_id):
    try:
        if not request.user.is_active:
            return redirect('login')
        requestdb = RequestDB.objects.get(id=req_id)
        request_property = RequestProperty.objects.get(requestid=requestdb.id)
        service_type = Service.objects.get(id=requestdb.serviceid)
        property_type = {'1': 'Agriculture Land', '2': 'Agriculture Farm House', '3': 'Residential Plot',
                         '4': 'Residential Flats', '5': 'Residential Villas/Independent Houses',
                         '6': 'Commercial/Industrial Open Spaces', '7': 'Commercial/Industrial Buildings'}
        obj = {'id': requestdb.id, 'name': requestdb.requestername, 'num': requestdb.requestermobile,
               'status': requestdb.requeststatus, 'service_type': service_type.name,
               'property_type': property_type[request_property.propertytype]}
        request_details = PreliminaryTask.objects.filter(requestid=requestdb.id)
        dharani = request_details.get(tasktype='D')
        dharani_details = getdetails(dharani)
        prohibited_land = request_details.get(tasktype='P')
        prohibited_land_details = getdetails(prohibited_land)
        encumbrance = request_details.get(tasktype='E')
        encumbrance_details = getdetails(encumbrance)
        urban_land = request_details.get(tasktype='U')
        urban_land_details = getdetails(urban_land)
        legal_cases = request_details.get(tasktype='L')
        legal_cases_details = getdetails(legal_cases)
        employees_list = Employee.objects.all().annotate(employee_name=Concat('firstname', Value(' '),
                                                                              'lastname')).values('id', 'employee_name')
        return render(request, "sidebar.html", {"template_name": "preliminary_verification.html",
                                                "request_obj": obj, 'dharani_details': dharani_details,
                                                'prohibited_land_details': prohibited_land_details,
                                                'encumbrance_details': encumbrance_details,
                                                'employees_list': employees_list,
                                                'urban_land_details': urban_land_details,
                                                'legal_cases_details': legal_cases_details,
                                                'req_id': req_id})
    except Exception as e:
        print(str(e))
        return redirect('tasks')


def dharani_details_entry(request, task_id):
    if not request.user.is_active:
        return redirect('login')
    task_details = PreliminaryTask.objects.get(id=task_id)
    try:
        if request.user.id not in [task_details.assignedto, task_details.verifiedby]:
            raise Exception('Access Denied')
        edit_access = False
        verify_access = False
        if request.user.id == task_details.assignedto:
            edit_access = True
        else:
            verify_access = True
        requestdb = RequestDB.objects.get(id=task_details.requestid)
        request_property = RequestProperty.objects.get(requestid=requestdb.id)
        service_type = Service.objects.get(id=requestdb.serviceid)
        dharani_details = Dharani.objects.filter(prelimtaskid=task_details.id).values()
        property_type = {'1': 'Agriculture Land', '2': 'Agriculture Farm House', '3': 'Residential Plot',
                         '4': 'Residential Flats', '5': 'Residential Villas/Independent Houses',
                         '6': 'Commercial/Industrial Open Spaces', '7': 'Commercial/Industrial Buildings'}
        obj = {'id': requestdb.id, 'name': requestdb.requestername, 'num': requestdb.requestermobile,
               'status': requestdb.requeststatus, 'service_type': service_type.name,
               'property_type': property_type[request_property.propertytype], 'task_id': task_details.id,
               'task_status': task_details.status, 'notes': task_details.notes if task_details.notes else '',
               'entryhours': task_details.entryhours, 'verifyhours': task_details.verifyhours,
               'remarks': task_details.remarks if task_details.remarks else '',
               'verify_status': task_details.verifystatus}
        return render(request, "sidebar.html", {"template_name": "dharani_details_entry.html", "request_obj": obj,
                                                "dharani_details": dharani_details, "edit_access": edit_access,
                                                "verify_access": verify_access})
    except Exception as e:
        messages.warning(request, str(e))
        return redirect(f'./preliminary-verification{task_details.requestid}')


def prohibited_details_entry(request, task_id):
    if not request.user.is_active:
        return redirect('login')
    print(task_id)
    task_details = PreliminaryTask.objects.get(id=task_id)
    print(task_details)
    try:
        if request.user.id not in [task_details.assignedto, task_details.verifiedby]:
            raise Exception('Access Denied')
        edit_access = False
        verify_access = False
        if request.user.id == task_details.assignedto:
            edit_access = True
        else:
            verify_access = True
        requestdb = RequestDB.objects.get(id=task_details.requestid)
        request_property = RequestProperty.objects.get(requestid=requestdb.id)
        service_type = Service.objects.get(id=requestdb.serviceid)
        prohibited_details = ProhibitedLand.objects.filter(prelimtaskid=task_details.id).values()
        property_type = {'1': 'Agriculture Land', '2': 'Agriculture Farm House', '3': 'Residential Plot',
                         '4': 'Residential Flats', '5': 'Residential Villas/Independent Houses',
                         '6': 'Commercial/Industrial Open Spaces', '7': 'Commercial/Industrial Buildings'}
        obj = {'id': requestdb.id, 'name': requestdb.requestername, 'num': requestdb.requestermobile,
               'status': requestdb.requeststatus, 'service_type': service_type.name,
               'property_type': property_type[request_property.propertytype], 'task_id': task_details.id,
               'task_status': task_details.status, 'notes': task_details.notes if task_details.notes else '',
               'entryhours': task_details.entryhours, 'verifyhours': task_details.verifyhours,
               'remarks': task_details.remarks if task_details.remarks else ''}
        landclassification = [{'name': 'Patta', 'value': 'P'}, {'name': 'Govt', 'value': 'G'},
                              {'name': 'Assigned', 'value': 'A'}, {'name': 'Others', 'value': 'O'}]
        return render(request, "sidebar.html", {"template_name": "prohibited_details_entry.html", "request_obj": obj,
                                                "prohibited_details": prohibited_details, "edit_access": edit_access,
                                                "verify_access": verify_access,
                                                "landclassification": landclassification})
    except Exception as e:
        messages.warning(request, str(e))
        return redirect(f'./preliminary-verification{task_details.requestid}')


def encumbrance_details_entry(request, task_id):
    if not request.user.is_active:
        return redirect('login')
    task_details = PreliminaryTask.objects.get(id=task_id)
    try:
        if request.user.id not in [task_details.assignedto, task_details.verifiedby]:
            raise Exception('Access Denied')
        edit_access = False
        verify_access = False
        if request.user.id == task_details.assignedto:
            edit_access = True
        else:
            verify_access = True
        requestdb = RequestDB.objects.get(id=task_details.requestid)
        request_property = RequestProperty.objects.get(requestid=requestdb.id)
        service_type = Service.objects.get(id=requestdb.serviceid)
        encumbrance_details = Encumbrance.objects.filter(requestid=task_details.requestid).values()
        property_type = {'1': 'Agriculture Land', '2': 'Agriculture Farm House', '3': 'Residential Plot',
                         '4': 'Residential Flats', '5': 'Residential Villas/Independent Houses',
                         '6': 'Commercial/Industrial Open Spaces', '7': 'Commercial/Industrial Buildings'}
        checklistquesn = Checklist.objects.filter(task='E').first()
        checklistans = Checklistanswer.objects.filter(task='E', requestid=requestdb.id).first()
        checklist = {}
        if checklistquesn:
            checklist.update({'answer': checklistans.answer if checklistans else None, 'question': checklistquesn.question})
        obj = {'id': requestdb.id, 'name': requestdb.requestername, 'num': requestdb.requestermobile,
               'status': requestdb.requeststatus, 'service_type': service_type.name,
               'property_type': property_type[request_property.propertytype], 'task_id': task_details.id,
               'task_status': task_details.status, 'notes': task_details.notes if task_details.notes else '',
               'entryhours': task_details.entryhours, 'verifyhours': task_details.verifyhours,
               'remarks': task_details.remarks if task_details.remarks else ''}
        return render(request, "sidebar.html", {"template_name": "encumbrance_details_entry.html", "request_obj": obj,
                                                "encumbrance_details": encumbrance_details, "edit_access": edit_access,
                                                "verify_access": verify_access, "checklist": checklist})
    except Exception as e:
        messages.warning(request, str(e))
        return redirect(f'./preliminary-verification{task_details.requestid}')


def urbanland_details_entry(request, task_id):
    if not request.user.is_active:
        return redirect('login')
    task_details = PreliminaryTask.objects.get(id=task_id)
    try:
        if request.user.id not in [task_details.assignedto, task_details.verifiedby]:
            raise Exception('Access Denied')
        edit_access = False
        verify_access = False
        if request.user.id == task_details.assignedto:
            edit_access = True
        else:
            verify_access = True
        requestdb = RequestDB.objects.get(id=task_details.requestid)
        request_property = RequestProperty.objects.get(requestid=requestdb.id)
        service_type = Service.objects.get(id=requestdb.serviceid)
        questions = Checklist.objects.filter(task='U').values()
        for question in questions:
            answer = Urbanland.objects.filter(requestid=task_details.requestid, qid=question['id']).last()
            question['answer'] = answer.response if answer else None
        property_type = {'1': 'Agriculture Land', '2': 'Agriculture Farm House', '3': 'Residential Plot',
                         '4': 'Residential Flats', '5': 'Residential Villas/Independent Houses',
                         '6': 'Commercial/Industrial Open Spaces', '7': 'Commercial/Industrial Buildings'}
        obj = {'id': requestdb.id, 'name': requestdb.requestername, 'num': requestdb.requestermobile,
               'status': requestdb.requeststatus, 'service_type': service_type.name,
               'property_type': property_type[request_property.propertytype], 'task_id': task_details.id,
               'task_status': task_details.status, 'notes': task_details.notes if task_details.notes else '',
               'entryhours': task_details.entryhours, 'verifyhours': task_details.verifyhours,
               'remarks': task_details.remarks if task_details.remarks else ''}
        yes_no = [{'value': 'Y', 'name': 'Yes'}, {'value': 'N', 'name': 'No'}]
        return render(request, "sidebar.html", {"template_name": "urban_land_details_entry.html", "request_obj": obj,
                                                "questions": questions, "edit_access": edit_access,
                                                "verify_access": verify_access, "yes_no": yes_no})
    except Exception as e:
        messages.warning(request, str(e))
        return redirect(f'./preliminary-verification{task_details.requestid}')


def legalcase_details_entry(request, task_id):
    if not request.user.is_active:
        return redirect('login')
    task_details = PreliminaryTask.objects.get(id=task_id)
    try:
        if request.user.id not in [task_details.assignedto, task_details.verifiedby]:
            raise Exception('Access Denied')
        edit_access = False
        verify_access = False
        if request.user.id == task_details.assignedto:
            edit_access = True
        else:
            verify_access = True
        requestdb = RequestDB.objects.get(id=task_details.requestid)
        request_property = RequestProperty.objects.get(requestid=requestdb.id)
        service_type = Service.objects.get(id=requestdb.serviceid)
        legalcase_details = LegalCase.objects.filter(requestid=task_details.requestid).values()
        property_type = {'1': 'Agriculture Land', '2': 'Agriculture Farm House', '3': 'Residential Plot',
                         '4': 'Residential Flats', '5': 'Residential Villas/Independent Houses',
                         '6': 'Commercial/Industrial Open Spaces', '7': 'Commercial/Industrial Buildings'}
        checklistquesn = Checklist.objects.filter(task='L').first()
        checklistans = Checklistanswer.objects.filter(task='L', requestid=requestdb.id).first()
        checklist = {}
        if checklistquesn:
            checklist.update(
                {'answer': checklistans.answer if checklistans else None, 'question': checklistquesn.question})
        obj = {'id': requestdb.id, 'name': requestdb.requestername, 'num': requestdb.requestermobile,
               'status': requestdb.requeststatus, 'service_type': service_type.name,
               'property_type': property_type[request_property.propertytype], 'task_id': task_details.id,
               'task_status': task_details.status, 'notes': task_details.notes if task_details.notes else '',
               'entryhours': task_details.entryhours, 'verifyhours': task_details.verifyhours,
               'remarks': task_details.remarks if task_details.remarks else ''}
        return render(request, "sidebar.html", {"template_name": "legalcase_details_entry.html", "request_obj": obj,
                                                "legalcase_details": legalcase_details, "edit_access": edit_access,
                                                "verify_access": verify_access, "checklist": checklist})
    except Exception as e:
        messages.warning(request, str(e))
        return redirect(f'./preliminary-verification{task_details.requestid}')

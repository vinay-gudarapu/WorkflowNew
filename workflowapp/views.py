import base64
import datetime
import io
import json
import logging
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from workflowapp.models import Employee, Holiday, HolidayDepartment, HolidayLocation, Team, TeamMember, PreliminaryTask, \
    Document, Dharani, RequestDB, ProhibitedLand, Encumbrance, LegalCase, Checklist, Checklistanswer, Urbanland
from allauth.account.utils import perform_login
from allauth.account import app_settings as allauth_settings


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            stream = io.BytesIO(request.body)
            dataObj = JSONParser().parse(stream)
            email = dataObj['email']
            password = dataObj['password']
            employee = Employee.objects.filter(email=email).first()
            if not employee:
                raise Exception('User not found')
            verification = pbkdf2_sha256.verify(password, employee.password)
            if not verification:
                raise Exception('Invalid password')
            perform_login(request._request, employee, allauth_settings.EMAIL_VERIFICATION, signup=False,
                          redirect_url=None, signal_kwargs=None)
            token = Token.objects.get(user_id=employee.id)
            response['token'] = token.key
            response['data'] = 'User logged in successfully'
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in login'
        response['error'] = str(e)
        logging.error("Error in login : ", str(e))
    return JsonResponse(response)


@api_view(['POST', 'GET'])
@authentication_classes([])
@permission_classes([])
def create_employee(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        password = pbkdf2_sha256.encrypt("Srinivas@1234")
        Employee.objects.create(firstname='srinivas', lastname='srinivas', email="srinivas@gmail.com", 
                                username="srinivas@gmail.com", password=password)
        response['data'] = 'Employee added successfully'
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in employee'
        response['error'] = str(e)
        logging.error("Error in employee : ", str(e))
    return JsonResponse(response)


@api_view(['POST', 'GET'])
@authentication_classes([])
@permission_classes([])
def employee(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            stream = io.BytesIO(request.body)
            dataObj = JSONParser().parse(stream)
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
            picture = dataObj.get('picture', None)
            Employee.objects.create(firstname=firstname, lastname=lastname, type=emp_type, departmentid=department,
                                    mobileoffice=mob_official, mobilepersonal=mob_personal, email=email, username=email,
                                    addressline1=address_line1, addressline2=address_line2, city=city, state=state,
                                    country=country, pincode=pincode, password=password, status=status,
                                    picture=picture)
            response['data'] = 'Employee added successfully'
        else:
            temp = []
            for emp in Employee.objects.all():
                obj = {'name': f'{emp.firstname} {emp.lastname}', 'mobile': emp.mobileoffice, 'dep': emp.departmentid,
                       'loc': emp.city, 'status': 'Active' if emp.status == 'A' else 'Inactive'}
                temp.append(obj)
            response['data'] = temp
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in employee'
        response['error'] = str(e)
        logging.error("Error in employee : ", str(e))
    return JsonResponse(response)


@api_view(['POST', 'GET'])
def holiday(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            stream = io.BytesIO(request.body)
            dataObj = JSONParser().parse(stream)
            name = dataObj['name']
            date = dataObj['date']
            holiday_type = dataObj['type']
            departments = dataObj['departments']
            state = dataObj['state']
            status = dataObj['status']
            hldy = Holiday.objects.create(holidaydate=date, holidayname=name, holidaytype=holiday_type,
                                          status=status)
            HolidayDepartment.objects.create(holidayid=hldy.id, departmentid=1)
            HolidayLocation.objects.create(holidayid=hldy.id, holidaylocation=state)
            response['data'] = 'Holiday added successfully'
        else:
            temp = []
            for hldy in Holiday.objects.all():
                holiday_dep = HolidayDepartment.objects.get(holidayid=hldy.id)
                obj = {'holiday': hldy.name, 'date': hldy.holidaydate,
                       'type': "Mandatory" if hldy.holidaytype == 'M' else 'Optional',
                       'dep': holiday_dep.departmentid, 'status': 'Active' if hldy.status == 'A' else 'Inactive'}
                temp.append(obj)
            response['data'] = temp
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in holiday'
        response['error'] = str(e)
        logging.error("Error in holiday : ", str(e))
    return JsonResponse(response)


@api_view(['POST', 'GET'])
def team(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            stream = io.BytesIO(request.body)
            dataObj = JSONParser().parse(stream)
            name = dataObj['name']
            teamlead = dataObj['team_lead']
            members = dataObj['members']
            department = dataObj['department']
            location = dataObj['location']
            status = dataObj['status']
            new_team = Team.objects.create(teamname=name, location=location, departmentid=1, teamlead=teamlead,
                                           status=status)
            for memb in members:
                TeamMember.objects.create(teamid=new_team.id, employeeid=memb)
            response['data'] = 'Team added successfully'
        else:
            temp = []
            for team in Team.objects.all():
                employee = Employee.objects.get(id=team.teamlead)
                obj = {'name': team.teamname, 'location': team.location,
                       'team_lead': f'{employee.firstname} {employee.lastname}',
                       'dep': team.departmentid, 'status': 'Active' if holiday.status == 'A' else 'Inactive'}
                temp.append(obj)
            response['data'] = temp
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in team'
        response['error'] = str(e)
        logging.error("Error in team : ", str(e))
    return JsonResponse(response)


@api_view(['GET'])
def getEmployee(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        emp_id = request.query_params.get('emp_id', None)
        employee = Employee.objects.get(id=emp_id)
        response['data'] = base64.b64encode(employee.picture).decode() if employee.picture else None
        response['name'] = f'{employee.firstname} {employee.lastname}'
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in team'
        response['error'] = str(e)
        logging.error("Error in team : ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def save_preliminary_task(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        dataObj = request.POST
        tasktype = dataObj['tasktype']
        to = dataObj['to']
        assign_to = dataObj['assign_to']
        req_id = dataObj['req_id']
        if to == "V":
            dictval = {'verifiedby': assign_to, 'status': "I"}
        else:
            dictval = {'assignedto': assign_to, 'assigneddate': datetime.datetime.now(), 'verifystatus': "I"}
        PreliminaryTask.objects.filter(requestid=req_id, tasktype=tasktype).update(**dictval)
        RequestDB.objects.filter(id=req_id).update(requeststatus='I')
        response['data'] = "Assigned successfully"
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in team'
        response['error'] = str(e)
        logging.error("Error in team : ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def save_image(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        dataObj = json.loads(request.POST['data'])
        requestid = dataObj['requestid']
        task = dataObj['task']
        filename = dataObj['filename']
        filetype = dataObj['filetype']
        filecontent = request.FILES['file'].read()
        Document.objects.create(requestid=requestid, task=task, filename=filename, filetype=filetype,
                                filecontent=filecontent)
        screens = []
        num = 1
        for doc in Document.objects.filter(requestid=requestid, task=task):
            file = base64.b64encode(doc.filecontent).decode()
            if file[0] == '/':
                file_content = f'data:image/jpg;base64,{file}'
                ext = 'jpg'
            elif file[0] == 'i':
                file_content = f'data:image/png;base64,{file}'
                ext = 'png'
            else:
                file_content = f'data:image/pdf;base64,{file}'
                ext = 'pdf'
            screens.append(
                {'screen': f'Screen {num}', 'file': file_content, 'function': f"openScreen(event, 'Screen_{num}')",
                 'ext': ext, 'doc_id': doc.id})
            num += 1
        response['data'] = screens
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in saving image'
        response['error'] = str(e)
        logging.error("Error in saving image : ", str(e))
    return JsonResponse(response)


@api_view(['GET'])
def get_screens(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        requestid = request.query_params.get('requestid', None)
        task = request.query_params.get('task', None)
        screens = []
        num = 1
        for doc in Document.objects.filter(requestid=requestid, task=task):
            file = base64.b64encode(doc.filecontent).decode()
            if file[0] == '/':
                file_content = f'data:image/jpg;base64,{file}'
                ext = 'jpg'
            elif file[0] == 'i':
                file_content = f'data:image/png;base64,{file}'
                ext = 'png'
            else:
                file_content = f'data:image/pdf;base64,{file}'
                ext = 'pdf'
            screens.append(
                {'screen': f'Screen {num}', 'file': file_content, 'function': f"openScreen(event, 'Screen_{num}')",
                 'ext': ext, 'doc_id': doc.id})
            num += 1
        response['data'] = screens
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in getting screens'
        response['error'] = str(e)
        logging.error("Error in getting screens : ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def delete_screen(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        dataObj = request.POST
        print(dataObj)
        requestid = dataObj['requestid']
        task = dataObj['task']
        doc_id = dataObj['doc_id']
        Document.objects.filter(id=doc_id).delete()
        screens = []
        num = 1
        for doc in Document.objects.filter(requestid=requestid, task=task):
            file = base64.b64encode(doc.filecontent).decode()
            if file[0] == '/':
                file_content = f'data:image/jpg;base64,{file}'
                ext = 'jpg'
            elif file[0] == 'i':
                file_content = f'data:image/png;base64,{file}'
                ext = 'png'
            else:
                file_content = f'data:image/pdf;base64,{file}'
                ext = 'pdf'
            screens.append(
                {'screen': f'Screen {num}', 'file': file_content, 'function': f"openScreen(event, 'Screen_{num}')",
                 'ext': ext, 'doc_id': doc.id})
            num += 1
        response['data'] = screens
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in getting screens'
        response['error'] = str(e)
        logging.error("Error in getting screens : ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def save_dharani_details(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        prelimtaskid = request.POST['prelimtaskid']
        status = request.POST['status']
        if 'data' in request.POST:
            dataObj = json.loads(request.POST['data'])
            delete_ids = json.loads(request.POST['delete_ids'])
            notes = request.POST['notes']
            hours = request.POST['hours']
            Dharani.objects.filter(id__in=delete_ids).delete()
            for data in dataObj:
                if not data['id']:
                    del data['id']
                    Dharani.objects.create(**data)
                else:
                    detail_id = data['id']
                    del data['id']
                    Dharani.objects.filter(id=detail_id).update(**data)
            update_data = {'notes': notes, 'entryhours': hours}
            if status:
                update_data.update({'status': status})
        else:
            remarks = request.POST['remarks']
            verifyhours = request.POST['verifyhours']
            update_data = {'remarks': remarks, 'verifyhours': verifyhours}
            if status:
                update_data.update({'verifystatus': status, 'completeddate': datetime.datetime.now()})
        PreliminaryTask.objects.filter(id=prelimtaskid).update(**update_data)
        response['data'] = "Dharani details saved successfully"
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in saving dharani details'
        response['error'] = str(e)
        logging.error("Error in saving dharani details : ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def save_preliminary_details(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        prelimtaskid = request.POST['prelimtaskid']
        status = request.POST['status']
        if 'data' in request.POST:
            dataObj = json.loads(request.POST['data'])
            delete_ids = json.loads(request.POST['delete_ids'])
            notes = request.POST['notes']
            hours = request.POST['hours']
            ProhibitedLand.objects.filter(id__in=delete_ids).delete()
            for data in dataObj:
                if not data['id']:
                    del data['id']
                    ProhibitedLand.objects.create(**data)
                else:
                    detail_id = data['id']
                    del data['id']
                    ProhibitedLand.objects.filter(id=detail_id).update(**data)
            update_data = {'notes': notes, 'entryhours': hours}
            if status:
                update_data.update({'status': status})
        else:
            remarks = request.POST['remarks']
            verifyhours = request.POST['verifyhours']
            update_data = {'remarks': remarks, 'verifyhours': verifyhours}
            if status:
                update_data.update({'verifystatus': status, 'completeddate': datetime.datetime.now()})
        PreliminaryTask.objects.filter(id=prelimtaskid).update(**update_data)
        response['data'] = "Preliminary details saved successfully"
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in saving preliminary task details'
        response['error'] = str(e)
        logging.error("Error in saving preliminary: ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def save_encumbrance_details(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        prelimtaskid = request.POST['prelimtaskid']
        status = request.POST['status']
        claimant = request.POST['claimant']
        if 'data' in request.POST:
            dataObj = json.loads(request.POST['data'])
            delete_ids = json.loads(request.POST['delete_ids'])
            notes = request.POST['notes']
            hours = request.POST['hours']
            Encumbrance.objects.filter(id__in=delete_ids).delete()
            for data in dataObj:
                if not data['id']:
                    del data['id']
                    Encumbrance.objects.create(**data)
                else:
                    detail_id = data['id']
                    del data['id']
                    Encumbrance.objects.filter(id=detail_id).update(**data)
            update_data = {'notes': notes, 'entryhours': hours}
            if status:
                update_data.update({'status': status})
        else:
            remarks = request.POST['remarks']
            verifyhours = request.POST['verifyhours']
            update_data = {'remarks': remarks, 'verifyhours': verifyhours}
            if status:
                update_data.update({'verifystatus': status, 'completeddate': datetime.datetime.now()})
        preliminary_task = PreliminaryTask.objects.filter(id=prelimtaskid)
        requestid = preliminary_task.first().requestid
        preliminary_task.update(**update_data)
        question = Checklist.objects.filter(task='E').first()
        answer = Checklistanswer.objects.filter(task='E', requestid=requestid, question=question.question)
        if answer:
            answer.update(answer=claimant)
        else:
            Checklistanswer.objects.create(task='E', requestid=requestid, question=question.question,
                                           choice=question.choice, answer=claimant)
        response['data'] = "Encumbrance details saved successfully"
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in saving encumbrance details'
        response['error'] = str(e)
        logging.error("Error in saving encumbrance: ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def save_legalcase_details(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        prelimtaskid = request.POST['prelimtaskid']
        status = request.POST['status']
        answer_data = request.POST['answer']
        if 'data' in request.POST:
            dataObj = json.loads(request.POST['data'])
            notes = request.POST['notes']
            hours = request.POST['hours']
            if answer_data == 'Y':
                delete_ids = json.loads(request.POST['delete_ids'])
                LegalCase.objects.filter(id__in=delete_ids).delete()
                for data in dataObj:
                    if not data['id']:
                        del data['id']
                        LegalCase.objects.create(**data)
                    else:
                        detail_id = data['id']
                        del data['id']
                        LegalCase.objects.filter(id=detail_id).update(**data)
            update_data = {'notes': notes, 'entryhours': hours}
            if status:
                update_data.update({'status': status})
        else:
            remarks = request.POST['remarks']
            verifyhours = request.POST['verifyhours']
            update_data = {'remarks': remarks, 'verifyhours': verifyhours}
            if status:
                update_data.update({'verifystatus': status, 'completeddate': datetime.datetime.now()})
        preliminary_task = PreliminaryTask.objects.filter(id=prelimtaskid)
        requestid = preliminary_task.first().requestid
        preliminary_task.update(**update_data)
        question = Checklist.objects.filter(task='L').first()
        answer = Checklistanswer.objects.filter(task='L', requestid=requestid, question=question.question)
        if answer:
            answer.update(answer=answer_data)
        else:
            Checklistanswer.objects.create(task='L', requestid=requestid, question=question.question,
                                           choice=question.choice, answer=answer_data)
        response['data'] = "Encumbrance details saved successfully"
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in saving encumbrance details'
        response['error'] = str(e)
        logging.error("Error in saving encumbrance: ", str(e))
    return JsonResponse(response)


@api_view(['POST'])
def save_urbanland_details(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        prelimtaskid = request.POST['prelimtaskid']
        status = request.POST['status']
        if 'data' in request.POST:
            dataObj = json.loads(request.POST['data'])
            notes = request.POST['notes']
            hours = request.POST['hours']
            for data in dataObj:
                if not Urbanland.objects.filter(requestid=data['requestid'], qid=data['qid']):
                    Urbanland.objects.create(**data)
                else:
                    Urbanland.objects.filter(requestid=data['requestid'], qid=data['qid']).update(**data)
            update_data = {'notes': notes, 'entryhours': hours}
            if status:
                update_data.update({'status': status})
        else:
            remarks = request.POST['remarks']
            verifyhours = request.POST['verifyhours']
            update_data = {'remarks': remarks, 'verifyhours': verifyhours}
            if status:
                update_data.update({'verifystatus': status, 'completeddate': datetime.datetime.now()})
        PreliminaryTask.objects.filter(id=prelimtaskid).update(**update_data)
        response['data'] = "Urban Land details saved successfully"
        response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in saving urban land details'
        response['error'] = str(e)
        logging.error("Error in saving urban land details: ", str(e))
    return JsonResponse(response)

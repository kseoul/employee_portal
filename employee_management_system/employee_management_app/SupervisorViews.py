from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
import json


from employee_management_app.models import CustomUser, Supervisors, Employees, FeedBackSupervisors,Teams, LeaveReportEmployees, LeaveApprovalEmployees, FeedBackEmployees


def supervisor_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    supervisor_obj = Supervisors.objects.get(id=user.supervisors.id)
    teams_obj = Teams.objects.get(id=supervisor_obj.team_id.id)
    employees_obj = Employees.objects.filter(team_id=teams_obj.id)
    employees_count = Employees.objects.filter(team_id=teams_obj.id).count()

    today_date = datetime.now().strftime("%Y-%m-%d")
    leaves_obj = LeaveReportEmployees.objects.all()
    
    pending_approvals_count = 0
    planned_leave_count = 0
    employee_leave_list = []
    employee_list = []
    for leave in leaves_obj:
        if(leave.employee_id.team_id.id == teams_obj.id) and (leave.leaveapprovalemployees.approval_date == None) and (leave.leave_status == 0):
            pending_approvals_count += 1

        if (leave.start_date.strftime("%Y-%m-%d") <= today_date) and (leave.end_date.strftime("%Y-%m-%d") >= today_date) and (leave.employee_id.team_id.id == teams_obj.id) and (leave.leave_status == 1):
            employee_leave_list.append(leave.employee_id.admin.first_name + " " + leave.employee_id.admin.last_name)
            planned_leave_count += 1
            if leave.employee_id.admin.username not in employee_list:
                employee_list.append(leave.employee_id.admin.username)

    unique_list = []

    [unique_list.append(x) for x in employee_leave_list if x not in unique_list]

    context={
        "employees_count": employees_count,
        "leave_count": planned_leave_count,
        "employee_list": employee_list,
        "employee_leave_list": unique_list,
        "today":today_date,
        "pending_approvals":pending_approvals_count,
        "team":teams_obj,
    }
    return render(request, "supervisor_template/supervisor_home_template.html", context)



def supervisor_take_attendance(request):
    return render(request, "supervisor_template/take_attendance_template.html")

def supervisor_feedback(request):
    supervisor_obj = Supervisors.objects.get(id=request.user.supervisors.id)
    feedback_data = FeedBackEmployees.objects.all()
    team = Teams.objects.get(id=request.user.supervisors.team_id.id)
    employees = Employees.objects.filter(team_id = team)
    employee_list = []
    for employee in employees:
        employee_list.append(employee.id)
    feedback_data = feedback_data.filter(employee_id__in=employee_list)

    context = {
        "feedback_data":feedback_data
    }
    return render(request, "supervisor_template/supervisor_feedback_template.html", context)

def supervisor_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('supervisor_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        supervisor_obj = Supervisors.objects.get(id=request.user.supervisors.id)

        try:
            add_feedback = FeedBackSupervisors(supervisor_id=supervisor_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('supervisor_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('supervisor_feedback')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_employees(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    # Employees enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    employees = Employees.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for employee in employees:
        data_small={"id":employee.admin.id, "name":employee.admin.first_name+" "+employee.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)




@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    employee_ids = request.POST.get("employee_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_employee = json.loads(employee_ids)
    # print(dict_employee[0]['id'])

    # print(employee_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
        attendance.save()

        for stud in json_employee:
            # Attendance of Individual Student saved on AttendanceReport Model
            employee = Employees.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(employee_id=employee, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def get_vacation(request):
    labels=[]
    data=[]

    pass

def supervisor_update_attendance(request):
    subjects = Subjects.objects.filter(supervisor_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "supervisor_template/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Employees enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # employees = Employees.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_employee(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for employee in attendance_data:
        data_small={"id":employee.employee_id.admin.id, "name":employee.employee_id.admin.first_name+" "+employee.employee_id.admin.last_name, "status":employee.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    employee_ids = request.POST.get("employee_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_employee = json.loads(employee_ids)

    try:
        
        for stud in json_employee:
            # Attendance of Individual Student saved on AttendanceReport Model
            employee = Employees.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(employee_id=employee, attendance_id=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

def chart(request):
    return render(request,'supervisor_template/chart.html')

def supervisor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    supervisor = Supervisors.objects.get(admin=user)

    context={
        "user": user,
        "supervisor": supervisor
    }
    return render(request, 'supervisor_template/supervisor_profile.html', context)


def supervisor_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('supervisor_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            supervisor = Supervisors.objects.get(admin=customuser.id)
            supervisor.address = address
            supervisor.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('supervisor_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('supervisor_profile')



def employee_leave_view(request):
    leaves = LeaveReportEmployees.objects.filter()
    supervisors = Supervisors.objects.all()
    teams = Teams.objects.all()
    approvals = LeaveApprovalEmployees.objects.all()

    context = {
        "leaves": leaves,
        "supervisors":supervisors,
        "teams":teams,
        "approvals":approvals,
    }
    return render(request, 'supervisor_template/supervisor_employee_leave_view.html', context)

def employee_leave_approve(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    user = CustomUser.objects.get(id=request.user.id)
    supervisor = Supervisors.objects.get(id=user.id)
    
    try:
        leave.leave_status = 1
        leave_approval = LeaveApprovalEmployees.objects.get(approval_id=leave.id)
        leave_approval.supervisor_id = supervisor
        leave.save()
        leave_approval.save()
        print("success")
        return redirect('supervisor_employee_leave_team_view')
    except:
        print("failed")
        return redirect('supervisor_employee_leave_team_view')


def employee_leave_reject(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    user = CustomUser.objects.get(id=request.user.id)
    supervisor = Supervisors.objects.get(id=user.supervisors.id)

    try:
        leave.leave_status = 2
        leave_approval = LeaveApprovalEmployees.objects.get(approval_id=leave.id)
        leave_approval.supervisor_id = supervisor
        leave.save()
        leave_approval.save()
        return redirect('supervisor_employee_leave_team_view')
    except:
        print("Failed")
        return redirect('supervisor_employee_leave_team_view')

def supervisor_employee_leave_team_view(request):
    #print(request.user.supervisors.id)
    teams = Teams.objects.get(id=request.user.supervisors.team_id.id)
    employees = Employees.objects.filter(team_id=teams.id)
    leaves = LeaveReportEmployees.objects.all()
    approvals = LeaveApprovalEmployees.objects.all()
    
    context = {
        "leaves": leaves,
        "teams":teams,
        "approvals":approvals,
        "employees":employees,
    }

    return render(request, 'supervisor_template/supervisor_employee_leave_team_view.html', context)

def kronos_entered(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    user = CustomUser.objects.get(id=request.user.id)
    #supervisor = Supervisors.objects.get(id=user.id)
    
    try:
        leave.kronos_status = True
        leave.save()
        print("Success Kronos")
        return redirect('supervisor_employee_leave_team_view')
    except:
        print("Failed Kronos")
        return redirect('supervisor_employee_leave_team_view')


def supervisor_employee_feedback_message(request):
    feedbacks = FeedBackEmployees.objects.all()
    print(feedbacks)
    team=Teams.objects.get(id=request.user.supervisors.team_id.id)
    employees = Employees.objects.filter(team_id = team)
    employee_list = []
    for employee in employees:
        employee_list.append(employee.id)
    feedbacks = feedbacks.filter(employee_id__in=employee_list)
    
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'supervisor_template/supervisor_employee_feedback_template.html', context)
'''
def supervisor_employee_feedback_message(request):
    supervisor_obj = Supervisors.objects.get(id=request.user.supervisors.id)
    feedback_data = FeedBackEmployees.objects.all()
    team = Teams.objects.get(id=request.user.supervisors.team_id.id)
    employees = Employees.objects.filter(team_id = team)
    employee_list = []
    for employee in employees:
        employee_list.append(employee.id)
    feedback_data = feedback_data.filter(employee_id__in=employee_list)

    context = {
        "feedback_data":feedback_data
    }
    #return render(request, 'hod_template/employee_feedback_template.html', context)
    return render(request, 'supervisor_template/supervisor_employee_feedback_template.html', context)
'''
@csrf_exempt
def supervisor_employee_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackEmployees.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")

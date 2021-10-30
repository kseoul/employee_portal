from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from datetime import datetime,timedelta # To Parse input DateTime into Python Date Time Object


from employee_management_app.models import CustomUser, Supervisors, Employees, LeaveReportEmployees, FeedBackEmployees, Teams


def employee_home(request):
    employee_obj = Employees.objects.get(admin=request.user.id)
    today_date = datetime.now()
    leave_requested = LeaveReportEmployees.objects.all()
    teams_obj = Teams.objects.get(id = request.user.employees.team_id.id)
    total_hours_approved = 0
    total_hours_pending_approval = 0
    for leave in leave_requested:
        if (leave.start_date.strftime("%Y") == today_date.strftime("%Y")) and (leave.leave_status == 1):
            total_hours_approved += leave.hours_calc
        else:
            total_hours_pending_approval += leave.hours_calc
    context = {
        "hours_approved":total_hours_approved,
        "pending_hours":total_hours_pending_approval,
        "team":teams_obj,
    }
    return render(request, "employee_template/employee_home_template.html",context)


def employee_view_attendance(request):
    employee = Employees.objects.get(admin=request.user.id) # Getting Logged in Employee Data
    return render(request, "employee_template/employee_view_attendance.html")


def employee_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('employee_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Employee Data Based on Logged in Data
        stud_obj = Employees.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, employee_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'employee_template/employee_attendance_data.html', context)
       

def employee_apply_leave(request):
    leave_data = LeaveReportEmployees.objects.filter(employee_id=request.user.employees.id)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'employee_template/employee_apply_leave.html', context)


def workdays(start,end,excluded=(6,7)):
    days = []
    while start <= end:
        if start.isoweekday() not in excluded:
            days.append(start)
        start += timedelta(days=1)
    return days

def employee_apply_leave_save(request):
    employee = Employees.objects.get(id=request.user.employees.id)
    team = Teams.objects.get(id=employee.team_id.id)
    supervisors = Supervisors.objects.filter(team_id=team.id)
    leaves = LeaveReportEmployees.objects.filter(employee_id=employee)
    try:
        supervisor_list = []
        for supervisor in supervisors:
            supervisor_list.append(supervisor.id)

    except:
        supervisors=None

    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('employee_apply_leave')
    else:
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_hours = request.POST.get('total_hours')
        leave_date = request.POST.get('leave_date')
        if (leave_date != ''):
            start_date = leave_date
            end_date = leave_date
        else:
            leave_date = None
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
        days_list = workdays(start_date,end_date)
        fail = 0
        for leave in leaves:
            leave_day_list = workdays(leave.start_date, leave.end_date)
            new_list = [i for i in days_list if i in leave_day_list]
            if (len(new_list) > 0):
                messages.error(request,"Failed to Apply")
                return redirect('employee_apply_leave')
        
        if (end_date < start_date):
            messages.error(request,"Failed to Apply")
            return redirect('employee_apply_leave')           
    
        leave_message = request.POST.get('leave_message')
        employee_obj = Employees.objects.get(admin=request.user.id)
        
        try:
            leave_report = LeaveReportEmployees(employee_id=employee_obj, leave_date=leave_date, start_date=start_date, end_date=end_date, hours_calc=total_hours, leave_message=leave_message, leave_status=0)
    
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('employee_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('employee_apply_leave')


def employee_feedback(request):
    employee_obj = Employees.objects.get(id=request.user.employees.id)
      
    feedback_data = FeedBackEmployees.objects.filter(employee_id=employee_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'employee_template/employee_feedback.html', context)


def employee_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('employee_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        employee_obj = Employees.objects.get(id=request.user.employees.id)
        if feedback == '':
            messages.error(request, "Failed to Send Feedback.")
            return redirect('employee_feedback')
        try:
            add_feedback = FeedBackEmployees(employee_id=employee_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('employee_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('employee_feedback')


def employee_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    employee = Employees.objects.get(admin=user)

    context={
        "user": user,
        "employee": employee
    }
    return render(request, 'employee_template/employee_profile.html', context)


def employee_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('employee_profile')
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

            employee = Employees.objects.get(admin=customuser.id)
            employee.address = address
            employee.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('employee_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('employee_profile')


def employee_view_result(request):
    employee = Employees.objects.get(admin=request.user.id)
    employee_result = EmployeeResult.objects.filter(employee_id=employee.id)
    context = {
        "employee_result": employee_result,
    }
    return render(request, "employee_template/employee_view_result.html", context)






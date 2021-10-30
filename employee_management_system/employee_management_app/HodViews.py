from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import datetime
import json

from employee_management_app.models import CustomUser, Supervisors,Employees,LeaveReportEmployees, FeedBackEmployees, FeedBackSupervisors, Teams, LeaveApprovalEmployees
from .forms import AddEmployeeForm, EditEmployeeForm

def admin_home(request):
    all_employee_count = Employees.objects.all().count()
    supervisor_count = Supervisors.objects.all().count()
    
    # For Supervisor
    supervisor_attendance_leave_list=[]
    supervisor_name_list=[]

    supervisors = Supervisors.objects.all()
    for supervisor in supervisors:
        supervisor_name_list.append(supervisor.admin.first_name)

    # For Employees
    employee_attendance_present_list=[]
    employee_attendance_leave_list=[]
    employee_name_list=[]

    employees = Employees.objects.all()
    for employee in employees:
        leaves = LeaveReportEmployees.objects.filter(employee_id=employee.id, leave_status=1).count()
        employee_attendance_leave_list.append(leaves)
        employee_name_list.append(employee.admin.first_name)


    context={
        "supervisor_attendance_leave_list": supervisor_attendance_leave_list,
        "supervisor_name_list": supervisor_name_list,
        "employee_attendance_present_list": employee_attendance_present_list,
        "employee_attendance_leave_list": employee_attendance_leave_list,
        "employee_name_list": employee_name_list,
    }
    return render(request, "hod_template/home_content.html")



def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    
    
def add_employee(request):
    form = AddEmployeeForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_employee_template.html', context)




def add_employee_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_employee')
    else:
        form = AddEmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            team = form.cleaned_data['team']

        # Getting Profile Pic first
        # First Check whether the file is selected or not
        # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)                
                user.employees.team_id = team
                user.employees.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Employee Added Successfully!")
                return redirect('add_employee')
            except:
                messages.error(request, "Failed to Add Employee!")
                return redirect('add_employee')
        else:
            return redirect('add_employee')


def manage_employee(request):
    employees = Employees.objects.all()
    context = {
        "employees": employees
    }
    return render(request, 'hod_template/manage_employee_template.html', context)


def edit_employee(request, employee_id):
    # Adding Employee ID into Session Variable
    request.session['employee_id'] = employee_id

    employee = Employees.objects.get(admin=employee_id)
    form = EditEmployeeForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = employee.admin.email
    form.fields['username'].initial = employee.admin.username
    form.fields['first_name'].initial = employee.admin.first_name
    form.fields['last_name'].initial = employee.admin.last_name
    form.fields['team'].initial = employee.team_id.id

    context = {
        "id": employee_id,
        "username": employee.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_employee_template.html", context)


def edit_employee_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        employee_id = request.session.get('employee_id')
        if employee_id == None:
            return redirect('/manage_employee')

        form = EditEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            team = form.cleaned_data['team']
            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=employee_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Employees Table
                employee_model = Employees.objects.get(admin=employee_id)
                employee_model.team_id = team
                if profile_pic_url != None:
                    employee_model.profile_pic = profile_pic_url
                employee_model.save()
                # Delete employee_id SESSION after the data is updated
                del request.session['employee_id']

                messages.success(request, "Employee Updated Successfully!")
                return redirect('/edit_employee/'+employee_id)
            except:
                messages.success(request, "Failed to Uupdate Employee.")
                return redirect('/edit_employee/'+employee_id)
        else:
            return redirect('/edit_employee/'+employee_id)


def delete_employee(request, employee_id):
    employee = Employees.objects.get(admin=employee_id)
    try:
        employee.delete()
        messages.success(request, "Employee Deleted Successfully.")
        return redirect('manage_employee')
    except:
        messages.error(request, "Failed to Delete Employee.")
        return redirect('manage_employee')


def add_supervisor(request):
    teams = Teams.objects.all()
    context = {
        "teams":teams
    }
    return render(request, "hod_template/add_supervisor_template.html",context)

def add_supervisor_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_supervisor')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        team = request.POST.get('teams')
        
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            teams=Teams.objects.get(id=team)
            user.supervisors.team_id = teams
            user.save()
            messages.success(request, "Supervisor Added Successfully!")
            return redirect('add_supervisor')
        except:
            messages.error(request, "Failed to Add Supervisor!")
            return redirect('add_supervisor')

def manage_supervisor(request):
    supervisors = Supervisors.objects.all()
    teams = Teams.objects.all()
    context = {
        "supervisors": supervisors,
        "teams":teams
    }
    return render(request, "hod_template/manage_supervisor_template.html", context)

def edit_supervisor(request, supervisor_id):
    supervisor = Supervisors.objects.get(admin=supervisor_id)
    teams = Teams.objects.all()
    context = {
        "supervisor": supervisor,
        "id": supervisor_id,
        "teams":teams
    }
    return render(request, "hod_template/edit_supervisor_template.html", context)

def edit_supervisor_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        supervisor_id = request.POST.get('supervisor_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        team = request.POST.get('teams')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=supervisor_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Supervisor Model
            supervisor_model = Supervisors.objects.get(admin=supervisor_id)
            team_id = Teams.objects.get(id=team)
            print(team_id)
            supervisor_model.team_id = team_id
            supervisor_model.save()

            messages.success(request, "Supervisor Updated Successfully.")
            return redirect('/edit_supervisor/'+supervisor_id)

        except:
            messages.error(request, "Failed to Update Supervisor.")
            return redirect('/edit_supervisor/'+supervisor_id)

def delete_supervisor(request, supervisor_id):
    supervisor = Supervisors.objects.get(admin=supervisor_id)
    try:
        supervisor.delete()
        messages.success(request, "Supervisor Deleted Successfully.")
        return redirect('manage_supervisor')
    except:
        messages.error(request, "Failed to Delete Supervisor.")
        return redirect('manage_supervisor')

def add_team(request):
    return render(request, 'hod_template/add_team_template.html')

def add_team_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_team')
    else:
        try:
            team_name = request.POST.get('team')
            team = Teams(team_name=team_name)
            team.save()
            messages.success(request, "Team Added Successfully!")
            return redirect('add_team')
        except:
            messages.error(request, "Failed to Add Team")
            return redirect('add_team')


def manage_team(request):
    teams = Teams.objects.all()
    context = {
        "teams": teams
    }
    return render(request, 'hod_template/manage_team_template.html', context)


def edit_team(request,team_id):
    teams = Teams.objects.get(id=team_id)
    context = {
        "teams": teams
    }
    return render(request, 'hod_template/edit_team_template.html', context)


def edit_team_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        teams = request.POST.get('team')
        teams_id = request.POST.get('team_id')
        print(teams)
        try:
            team = Teams.objects.get(id=teams_id)
            team.team_name = teams
            team.save()
            messages.success(request, "Team Updated Successfully.")
            return HttpResponseRedirect(reverse("edit_team", kwargs={"team_id":teams_id}))

        except:
            messages.error(request, "Failed to Update Team.")
            return HttpResponseRedirect(reverse("edit_team", kwargs={"team_id":teams_id}))
            



def delete_team(request, team_id):
    team = Teams.objects.get(id=team_id)
    try:
        team.delete()
        messages.success(request, "Team Deleted Successfully.")
        return redirect('manage_team')
    except:
        messages.error(request, "Failed to Delete Team.")
        return redirect('manage_team')

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def employee_feedback_message(request):
    feedbacks = FeedBackEmployees.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/employee_feedback_template.html', context)

@csrf_exempt
def employee_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackEmployees.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def supervisor_feedback_message(request):
    feedbacks = FeedBackSupervisors.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/supervisor_feedback_template.html', context)


@csrf_exempt
def supervisor_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackSupervisors.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def employee_leave_view(request):
    leaves = LeaveReportEmployees.objects.all()
    supervisors = Supervisors.objects.all()
    teams = Teams.objects.all()
    approvals = LeaveApprovalEmployees.objects.all()

    context = {
        "leaves": leaves,
        "supervisors":supervisors,
        "teams":teams,
        "approvals":approvals,
    }
    return render(request, 'hod_template/employee_leave_view.html', context)

def employee_leave_approve(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    user = CustomUser.objects.get(id=request.user.id)
    supervisor = Supervisors.objects.get(id=request.user.supervisors.id)
    
    try:
        leave.leave_status = 1
        leave_approval = LeaveApprovalEmployees.objects.get(approval_id=leave)
        leave_approval.supervisor_id = supervisor
        leave_approval.approval_date = datetime.datetime.now()
        leave.save()
        leave_approval.save()
        print("success")
        return redirect('employee_leave_view')
    except:
        print("failed")
        return redirect('employee_leave_view')


def employee_leave_reject(request, leave_id):
    leave = LeaveReportEmployees.objects.get(id=leave_id)
    supervisor = Supervisors.objects.get(id=request.user.supervisors.id)
    leave.leave_status = 2
    leave_approval = LeaveApprovalEmployees.objects.get(approval_id=leave)
    leave_approval.supervisor_id = supervisor
    leave_approval.approval_date = datetime.datetime.now()
    leave.save()
    leave_approval.save()
    return redirect('employee_leave_view')

###################

def admin_view_attendance(request):
    return render(request, "hod_template/admin_view_attendance.html")


@csrf_exempt
def admin_get_attendance_dates(request):
    # Only Passing Employee Id and Employee Name Only
    list_data = []
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_employee(request):
    # Getting Values from Ajax POST 'Fetch Employee'

    list_data = []

    for employee in attendance_data:
        data_small={"id":employee.employee_id.admin.id, "name":employee.employee_id.admin.first_name+" "+employee.employee_id.admin.last_name, "status":employee.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def supervisor_profile(request):
    pass


def employee_profile(requtest):
    pass

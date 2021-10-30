from django.urls import path, include
from . import views
from . import HodViews, SupervisorViews, EmployeeViews


urlpatterns = [
    path('', views.loginPage, name="login"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
    path('add_employee/', HodViews.add_employee, name="add_employee"),
    path('add_employee_save/', HodViews.add_employee_save, name="add_employee_save"),
    path('edit_employee/<employee_id>', HodViews.edit_employee, name="edit_employee"),
    path('edit_employee_save/', HodViews.edit_employee_save, name="edit_employee_save"),
    path('manage_employee/', HodViews.manage_employee, name="manage_employee"),
    path('delete_employee/<employee_id>/', HodViews.delete_employee, name="delete_employee"),
    path('add_supervisor/', HodViews.add_supervisor, name="add_supervisor"),
    path('add_supervisor_save/', HodViews.add_supervisor_save, name="add_supervisor_save"),
    path('manage_supervisor/', HodViews.manage_supervisor, name="manage_supervisor"),
    path('edit_supervisor/<supervisor_id>/', HodViews.edit_supervisor, name="edit_supervisor"),
    path('edit_supervisor_save/', HodViews.edit_supervisor_save, name="edit_supervisor_save"),
    path('delete_supervisor/<supervisor_id>/', HodViews.delete_supervisor, name="delete_supervisor"),
    path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),
    path('employee_feedback_message/', HodViews.employee_feedback_message, name="employee_feedback_message"),
    path('employee_feedback_message_reply/', HodViews.employee_feedback_message_reply, name="employee_feedback_message_reply"),
    path('supervisor_feedback_message/', HodViews.supervisor_feedback_message, name="supervisor_feedback_message"),
    path('supervisor_feedback_message_reply/', HodViews.supervisor_feedback_message_reply, name="supervisor_feedback_message_reply"),
    path('employee_leave_view/', HodViews.employee_leave_view, name="employee_leave_view"),
    path('employee_leave_approve/<leave_id>/', HodViews.employee_leave_approve, name="employee_leave_approve"),
    path('employee_leave_reject/<leave_id>/', HodViews.employee_leave_reject, name="employee_leave_reject"),
    path('admin_view_attendance/', HodViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HodViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_employee/', HodViews.admin_get_attendance_employee, name="admin_get_attendance_employee"),
    path('add_team/', HodViews.add_team, name="add_team"),
    path('add_team_save/', HodViews.add_team_save, name="add_team_save"),
    path('manage_team/', HodViews.manage_team, name="manage_team"),
    path('edit_team/<team_id>/', HodViews.edit_team, name="edit_team"),
    path('edit_team_save/', HodViews.edit_team_save, name="edit_team_save"),
    path('delete_team/<team_id>/', HodViews.delete_team, name="delete_team"),


    # URLs for Employees
    path('employee_home/', EmployeeViews.employee_home, name="employee_home"),
    path('employee_view_attendance/', EmployeeViews.employee_view_attendance, name="employee_view_attendance"),
    path('employee_view_attendance_post/', EmployeeViews.employee_view_attendance_post, name="employee_view_attendance_post"),
    path('employee_apply_leave/', EmployeeViews.employee_apply_leave, name="employee_apply_leave"),
    path('employee_apply_leave_save/', EmployeeViews.employee_apply_leave_save, name="employee_apply_leave_save"),
    path('employee_feedback/', EmployeeViews.employee_feedback, name="employee_feedback"),
    path('employee_feedback_save/', EmployeeViews.employee_feedback_save, name="employee_feedback_save"),
    path('employee_profile/', EmployeeViews.employee_profile, name="employee_profile"),
    path('employee_profile_update/', EmployeeViews.employee_profile_update, name="employee_profile_update"),
    path('employee_view_result/', EmployeeViews.employee_view_result, name="employee_view_result"),


    # URLS for Supervisor
    path('supervisor_home/', SupervisorViews.supervisor_home, name="supervisor_home"),
    path('supervisor_take_attendance/', SupervisorViews.supervisor_take_attendance, name="supervisor_take_attendance"),
    path('get_employees/', SupervisorViews.get_employees, name="get_employees"),
    path('save_attendance_data/', SupervisorViews.save_attendance_data, name="save_attendance_data"),
    path('supervisor_update_attendance/', SupervisorViews.supervisor_update_attendance, name="supervisor_update_attendance"),
    path('get_attendance_dates/', SupervisorViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_employee/', SupervisorViews.get_attendance_employee, name="get_attendance_employee"),
    path('update_attendance_data/', SupervisorViews.update_attendance_data, name="update_attendance_data"),
    path('supervisor_feedback/', SupervisorViews.supervisor_feedback, name="supervisor_feedback"),
    path('supervisor_feedback_save/', SupervisorViews.supervisor_feedback_save, name="supervisor_feedback_save"),
    path('supervisor_profile/', SupervisorViews.supervisor_profile, name="supervisor_profile"),
    path('supervisor_profile_update/', SupervisorViews.supervisor_profile_update, name="supervisor_profile_update"),
    path('supervisor_employee_leave_view/', SupervisorViews.employee_leave_view, name="supervisor_employee_leave_view"),
    path('supervisor_employee_leave_approve/<leave_id>/', SupervisorViews.employee_leave_approve, name="supervisor_employee_leave_approve"),
    path('supervisor_employee_leave_reject/<leave_id>/', SupervisorViews.employee_leave_reject, name="supervisor_employee_leave_reject"),
    path('supervisor_employee_leave_team_view/', SupervisorViews.supervisor_employee_leave_team_view, name="supervisor_employee_leave_team_view"),
    path('kronos_entered/<leave_id>', SupervisorViews.kronos_entered, name="kronos_entered"),
    path('supervisor_employee_feedback_message/', SupervisorViews.supervisor_employee_feedback_message, name="supervisor_employee_feedback_message"),
    path('supervisor_employee_feedback_message_reply/', SupervisorViews.supervisor_employee_feedback_message_reply, name="supervisor_employee_feedback_message_reply"),
]




""" 

path('add_course/', HodViews.add_course, name="add_course"),
path('add_course_save/', HodViews.add_course_save, name="add_course_save"),
path('manage_course/', HodViews.manage_course, name="manage_course"),
path('edit_course/<course_id>/', HodViews.edit_course, name="edit_course"),
path('edit_course_save/', HodViews.edit_course_save, name="edit_course_save"),
path('delete_course/<course_id>/', HodViews.delete_course, name="delete_course"),
path('manage_session/', HodViews.manage_session, name="manage_session"),
path('add_session/', HodViews.add_session, name="add_session"),
path('add_session_save/', HodViews.add_session_save, name="add_session_save"),
path('edit_session/<session_id>', HodViews.edit_session, name="edit_session"),
path('edit_session_save/', HodViews.edit_session_save, name="edit_session_save"),
path('delete_session/<session_id>/', HodViews.delete_session, name="delete_session"),



    path('supervisor_leave_view/', HodViews.supervisor_leave_view, name="supervisor_leave_view"),
    path('supervisor_leave_approve/<leave_id>/', HodViews.supervisor_leave_approve, name="supervisor_leave_approve"),
    path('supervisor_leave_reject/<leave_id>/', HodViews.supervisor_leave_reject, name="supervisor_leave_reject"),



# URSL for employee
path('employee_home/', employeeViews.employee_home, name="employee_home"),
path('employee_view_attendance/', employeeViews.employee_view_attendance, name="employee_view_attendance"),
path('employee_view_attendance_post/', employeeViews.employee_view_attendance_post, name="employee_view_attendance_post"),
path('employee_apply_leave/', employeeViews.employee_apply_leave, name="employee_apply_leave"),
path('employee_apply_leave_save/', employeeViews.employee_apply_leave_save, name="employee_apply_leave_save"),
path('employee_feedback/', employeeViews.employee_feedback, name="employee_feedback"),
path('employee_feedback_save/', employeeViews.employee_feedback_save, name="employee_feedback_save"),
path('employee_profile/', employeeViews.employee_profile, name="employee_profile"),
path('employee_profile_update/', employeeViews.employee_profile_update, name="employee_profile_update"),
path('employee_view_result/', employeeViews.employee_view_result, name="employee_view_result"),
"""
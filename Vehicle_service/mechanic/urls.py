from django.urls import path
from Vehicle_service.mechanic import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('mechanicsignup', views.mechanic_signup_view, name='mechanicsignup'),
    path('mechaniclogin', LoginView.as_view(template_name='vehicle/../../templates/mechanic/mechaniclogin.html'), name='mechaniclogin'),
    path('mechanic-dashboard', views.mechanic_dashboard_view, name='mechanic-dashboard'),
    path('mechanic-work-assigned', views.mechanic_work_assigned_view, name='mechanic-work-assigned'),
    path('mechanic-update-status/<int:pk>', views.mechanic_update_status_view, name='mechanic-update-status'),
    path('mechanic-feedback', views.mechanic_feedback_view, name='mechanic-feedback'),
    path('mechanic-salary', views.mechanic_salary_view, name='mechanic-salary'),
    path('mechanic-profile', views.mechanic_profile_view, name='mechanic-profile'),
    path('edit-mechanic-profile', views.edit_mechanic_profile_view, name='edit-mechanic-profile'),
    path('mechanic-attendance', views.mechanic_attendance_view, name='mechanic-attendance'),
    path('admin-mechanic', views.admin_mechanic_view, name='admin-mechanic'),
    path('admin-view-mechanic', views.admin_view_mechanic_view, name='admin-view-mechanic'),
    path('delete-mechanic/<int:pk>', views.delete_mechanic_view, name='delete-mechanic'),
    path('update-mechanic/<int:pk>', views.update_mechanic_view, name='update-mechanic'),
    path('admin-add-mechanic', views.admin_add_mechanic_view, name='admin-add-mechanic'),
    path('admin-approve-mechanic', views.admin_approve_mechanic_view, name='admin-approve-mechanic'),
    path('approve-mechanic/<int:pk>', views.approve_mechanic_view, name='approve-mechanic'),
    path('delete-mechanic/<int:pk>', views.delete_mechanic_view, name='delete-mechanic'),
    path('admin-view-mechanic-salary', views.admin_view_mechanic_salary_view,
         name='admin-view-mechanic-salary'),
    path('update-salary/<int:pk>', views.update_salary_view, name='update-salary'),
    path('admin-mechanic-attendance', views.admin_mechanic_attendance_view, name='admin-mechanic-attendance'),
]

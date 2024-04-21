from django.shortcuts import redirect
from Vehicle_service.customer import forms, models
from Vehicle_service.admin_user import forms, models
from Vehicle_service.mechanic import forms, models
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render


# Create your views here.

def mechanic_signup_view(request):
    userForm = forms.MechanicUserForm()
    mechanicForm = forms.MechanicForm()
    mydict = {'userForm': userForm, 'mechanicForm': mechanicForm}
    if request.method == 'POST':
        userForm = forms.MechanicUserForm(request.POST)
        mechanicForm = forms.MechanicForm(request.POST, request.FILES)
        if userForm.is_valid() and mechanicForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            mechanic = mechanicForm.save(commit=False)
            mechanic.user = user
            mechanic.save()
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
        return HttpResponseRedirect('mechaniclogin')
    return render(request, 'vehicle/../../templates/mechanic/mechanicsignup.html', context=mydict)


def is_mechanic(user):
    return user.groups.filter(name='MECHANIC').exists()


@login_required(login_url='adminlogin')
def admin_mechanic_view(request):
    return render(request, 'vehicle/../../templates/admin/admin_mechanic.html')


@login_required(login_url='adminlogin')
def admin_approve_mechanic_view(request):
    mechanics = models.Mechanic.objects.all().filter(status=False)
    return render(request, 'vehicle/../../templates/admin/admin_approve_mechanic.html', {'mechanics': mechanics})


@login_required(login_url='adminlogin')
def approve_mechanic_view(request, pk):
    mechanicSalary = forms.MechanicSalaryForm()
    if request.method == 'POST':
        mechanicSalary = forms.MechanicSalaryForm(request.POST)
        if mechanicSalary.is_valid():
            mechanic = models.Mechanic.objects.get(id=pk)
            mechanic.salary = mechanicSalary.cleaned_data['salary']
            mechanic.status = True
            mechanic.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-mechanic')
    return render(request, 'vehicle/../../templates/admin/admin_approve_mechanic_details.html', {'mechanicSalary': mechanicSalary})


@login_required(login_url='adminlogin')
def delete_mechanic_view(request, pk):
    mechanic = models.Mechanic.objects.get(id=pk)
    user = models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('admin-approve-mechanic')


@login_required(login_url='adminlogin')
def admin_add_mechanic_view(request):
    userForm = forms.MechanicUserForm()
    mechanicForm = forms.MechanicForm()
    mechanicSalary = forms.MechanicSalaryForm()
    mydict = {'userForm': userForm, 'mechanicForm': mechanicForm, 'mechanicSalary': mechanicSalary}
    if request.method == 'POST':
        userForm = forms.MechanicUserForm(request.POST)
        mechanicForm = forms.MechanicForm(request.POST, request.FILES)
        mechanicSalary = forms.MechanicSalaryForm(request.POST)
        if userForm.is_valid() and mechanicForm.is_valid() and mechanicSalary.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            mechanic = mechanicForm.save(commit=False)
            mechanic.user = user
            mechanic.status = True
            mechanic.salary = mechanicSalary.cleaned_data['salary']
            mechanic.save()
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-mechanic')
        else:
            print('problem in form')
    return render(request, 'vehicle/../../templates/admin/admin_add_mechanic.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_view_mechanic_view(request):
    mechanics = models.Mechanic.objects.all()
    return render(request, 'vehicle/../../templates/admin/admin_view_mechanic.html', {'mechanics': mechanics})


@login_required(login_url='adminlogin')
def delete_mechanic_view(request, pk):
    mechanic = models.Mechanic.objects.get(id=pk)
    user = models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('admin-view-mechanic')


@login_required(login_url='adminlogin')
def update_mechanic_view(request, pk):
    mechanic = models.Mechanic.objects.get(id=pk)
    user = User.objects.get(id=mechanic.user_id)
    userForm = forms.MechanicUserForm(instance=user)
    mechanicForm = forms.MechanicForm(request.FILES, instance=mechanic)
    mydict = {'userForm': userForm, 'mechanicForm': mechanicForm}
    if request.method == 'POST':
        userForm = forms.MechanicUserForm(request.POST, instance=user)
        mechanicForm = forms.MechanicForm(request.POST, request.FILES, instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('admin-view-mechanic')
    return render(request, 'vehicle/../../templates/admin/update_mechanic.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_view_mechanic_salary_view(request):
    mechanics = models.Mechanic.objects.all()
    return render(request, 'vehicle/../../templates/admin/admin_view_mechanic_salary.html', {'mechanics': mechanics})


@login_required(login_url='adminlogin')
def update_salary_view(request, pk):
    mechanicSalary = forms.MechanicSalaryForm()
    if request.method == 'POST':
        mechanicSalary = forms.MechanicSalaryForm(request.POST)
        if mechanicSalary.is_valid():
            mechanic = models.Mechanic.objects.get(id=pk)
            mechanic.salary = mechanicSalary.cleaned_data['salary']
            mechanic.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-mechanic-salary')
    return render(request, 'vehicle/../../templates/admin/admin_approve_mechanic_details.html', {'mechanicSalary': mechanicSalary})


@login_required(login_url='adminlogin')
def admin_mechanic_attendance_view(request):
    return render(request, 'vehicle/../../templates/admin/admin_mechanic_attendance.html')


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_dashboard_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    work_in_progress = models.Request.objects.all().filter(mechanic_id=mechanic.id, status='Repairing').count()
    work_completed = models.Request.objects.all().filter(mechanic_id=mechanic.id, status='Repairing Done').count()
    new_work_assigned = models.Request.objects.all().filter(mechanic_id=mechanic.id, status='Approved').count()
    dict = {
        'work_in_progress': work_in_progress,
        'work_completed': work_completed,
        'new_work_assigned': new_work_assigned,
        'salary': mechanic.salary,
        'mechanic': mechanic,
    }
    return render(request, 'vehicle/../../templates/mechanic/mechanic_dashboard.html', context=dict)


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_work_assigned_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    works = models.Request.objects.all().filter(mechanic_id=mechanic.id)
    return render(request, 'vehicle/../../templates/mechanic/mechanic_work_assigned.html', {'works': works, 'mechanic': mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_update_status_view(request, pk):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    updateStatus = forms.MechanicUpdateStatusForm()
    if request.method == 'POST':
        updateStatus = forms.MechanicUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.status = updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/mechanic-work-assigned')
    return render(request, 'vehicle/../../templates/mechanic/mechanic_update_status.html', {'updateStatus': updateStatus, 'mechanic': mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_attendance_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    attendaces = models.Attendance.objects.all().filter(mechanic=mechanic)
    return render(request, 'vehicle/../../templates/mechanic/mechanic_view_attendance.html', {'attendaces': attendaces, 'mechanic': mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_feedback_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    feedback = forms.FeedbackForm()
    if request.method == 'POST':
        feedback = forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request, 'vehicle/feedback_sent.html', {'mechanic': mechanic})
    return render(request, 'vehicle/../../templates/mechanic/mechanic_feedback.html', {'feedback': feedback, 'mechanic': mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_salary_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    workdone = models.Request.objects.all().filter(mechanic_id=mechanic.id).filter(
        Q(status="Repairing Done") | Q(status="Released"))
    return render(request, 'vehicle/../../templates/mechanic/mechanic_salary.html', {'workdone': workdone, 'mechanic': mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_profile_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    return render(request, 'vehicle/../../templates/mechanic/mechanic_profile.html', {'mechanic': mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def edit_mechanic_profile_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    user = User.objects.get(id=mechanic.user_id)
    userForm = forms.MechanicUserForm(instance=user)
    mechanicForm = forms.MechanicForm(request.FILES, instance=mechanic)
    mydict = {'userForm': userForm, 'mechanicForm': mechanicForm, 'mechanic': mechanic}
    if request.method == 'POST':
        userForm = forms.MechanicUserForm(request.POST, instance=user)
        mechanicForm = forms.MechanicForm(request.POST, request.FILES, instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('mechanic-profile')
    return render(request, 'vehicle/../../templates/mechanic/edit_mechanic_profile.html', context=mydict)

from django.contrib import auth
from django.contrib.auth import user_logged_out
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from Vehicle_service.customer import forms, models
from Vehicle_service.admin_user import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'vehicle/index.html')


# for showing signup/login button for customer


# for showing signup/login button for mechanics
def mechanicsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'vehicle/../../templates/mechanic/mechanicsclick.html')


# for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


# for checking user customer, mechanic or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def is_mechanic(user):
    return user.groups.filter(name='MECHANIC').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')
    elif is_mechanic(request.user):
        accountapproval = models.Mechanic.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('mechanic-dashboard')
        else:
            return render(request, 'vehicle/../../templates/mechanic/mechanic_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')


# ============================================================================================
# ADMIN RELATED views start
# ============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    customers = []
    for enq in enquiry:
        customer = models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict = {
        'total_customer': models.Customer.objects.all().count(),
        'total_mechanic': models.Mechanic.objects.all().count(),
        'total_request': models.Request.objects.all().count(),
        'total_feedback': models.Feedback.objects.all().count(),
        'data': zip(customers, enquiry),
    }
    return render(request, 'vehicle/../../templates/admin/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request, 'vehicle/../../templates/admin/admin_customer.html')


@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers = models.Customer.objects.all()
    return render(request, 'vehicle/../../templates/admin/admin_view_customer.html', {'customers': customers})


@login_required(login_url='adminlogin')
def delete_customer_view(request, pk):
    customer = models.Customer.objects.get(id=pk)
    user = models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request, pk):
    customer = models.Customer.objects.get(id=pk)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(request.FILES, instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, request.FILES, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request, 'vehicle/../../templates/admin/update_customer.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request, 'vehicle/../../templates/admin/admin_add_customer.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    customers = []
    for enq in enquiry:
        customer = models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request, 'vehicle/../../templates/admin/admin_view_customer_enquiry.html', {'data': zip(customers, enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry = models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers = []
    for enq in enquiry:
        print(enq)
        customer = models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request, 'vehicle/../../templates/admin/admin_view_customer_invoice.html', {'data': zip(customers, enquiry)})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request, 'vehicle/../../templates/admin/admin_request.html')


@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    customers = []
    for enq in enquiry:
        customer = models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request, 'vehicle/../../templates/admin/admin_view_request.html', {'data': zip(customers, enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request, pk):
    adminenquiry = forms.AdminApproveRequestForm()
    if request.method == 'POST':
        adminenquiry = forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.mechanic = adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost = adminenquiry.cleaned_data['cost']
            enquiry_x.status = adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request, 'vehicle/../../templates/admin/admin_approve_request_details.html', {'adminenquiry': adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request, pk):
    requests = models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')


@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry = forms.RequestForm()
    adminenquiry = forms.AdminRequestForm()
    mydict = {'enquiry': enquiry, 'adminenquiry': adminenquiry}
    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        adminenquiry = forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.customer = adminenquiry.cleaned_data['customer']
            enquiry_x.mechanic = adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost = adminenquiry.cleaned_data['cost']
            enquiry_x.status = 'Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request, 'vehicle/../../templates/admin/admin_add_request.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry = models.Request.objects.all().filter(status='Pending')
    return render(request, 'vehicle/../../templates/admin/admin_approve_request.html', {'enquiry': enquiry})


@login_required(login_url='adminlogin')
def approve_request_view(request, pk):
    adminenquiry = forms.AdminApproveRequestForm()
    if request.method == 'POST':
        adminenquiry = forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.mechanic = adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost = adminenquiry.cleaned_data['cost']
            enquiry_x.status = adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request, 'vehicle/../../templates/admin/admin_approve_request_details.html', {'adminenquiry': adminenquiry})


@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    customers = []
    for enq in enquiry:
        customer = models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request, 'vehicle/../../templates/admin/admin_view_service_cost.html', {'data': zip(customers, enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request, pk):
    updateCostForm = forms.UpdateCostForm()
    if request.method == 'POST':
        updateCostForm = forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.cost = updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request, 'vehicle/../../templates/admin/update_cost.html', {'updateCostForm': updateCostForm})


@login_required(login_url='adminlogin')
def admin_take_attendance_view(request):
    mechanics = models.Mechanic.objects.all().filter(status=True)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('present_status')
            date = form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel = models.Attendance()

                AttendanceModel.date = date
                AttendanceModel.present_status = Attendances[i]
                print(mechanics[i].id)
                print(int(mechanics[i].id))
                mechanic = models.Mechanic.objects.get(id=int(mechanics[i].id))
                AttendanceModel.mechanic = mechanic
                AttendanceModel.save()
            return redirect('admin-view-attendance')
        else:
            print('form invalid')
    return render(request, 'vehicle/../../templates/admin/admin_take_attendance.html', {'mechanics': mechanics, 'aform': aform})


@login_required(login_url='adminlogin')
def admin_view_attendance_view(request):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.all().filter(date=date)
            mechanicdata = models.Mechanic.objects.all().filter(status=True)
            mylist = zip(attendancedata, mechanicdata)
            return render(request, 'vehicle/../../templates/admin/admin_view_attendance_page.html', {'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'vehicle/../../templates/admin/admin_view_attendance_ask_date.html', {'form': form})


@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports = models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict = {
        'reports': reports,
    }
    return render(request, 'vehicle/../../templates/admin/admin_report.html', context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback = models.Feedback.objects.all().order_by('-id')
    return render(request, 'vehicle/../../templates/admin/admin_feedback.html', {'feedback': feedback})


# for aboutus and contact
def aboutus_view(request):
    return render(request, 'vehicle/aboutus.html')


def contactus_view(request):
    sub = forms.ContactUsForm
    if request.method == 'POST':
        sub = forms.ContactUsForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'vehicle/contactussuccess.html')
    return render(request, 'vehicle/contactus.html', {'form': sub})


# def logout(request):
#     if request.method == 'POST':
#         auth.logout(request)
#         request.session.flush()
#         return redirect('home')
#
#     return render(request, 'vehicle/index.html')

# def logout(request):
#     if request.method == 'POST':
#         # This is to handle the POST request, if needed.
#         user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
#         clear_session(request)
#
#     return render(request, 'vehicle/index.html')  # Render the index page
#
#
# # Use LogoutView for handling logout
# logout_view = LogoutView.as_view(next_page='home')

class LogoutUserView(auth_views.LogoutView):
    next_page = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return super().post(request, *args, **kwargs)


# @receiver(user_logged_out)
# def clear_session(sender, request, **kwargs):
#     request.session.clear()

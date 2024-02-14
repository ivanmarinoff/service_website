from django.shortcuts import render, redirect
from . import forms, models
from Vehicle_service.customer import forms, models
from Vehicle_service.admin_user import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q


def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'vehicle/customerclick.html')

def customer_signup_view(request):
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
        return HttpResponseRedirect('customerlogin')
    return render(request, 'vehicle/customersignup.html', context=mydict)


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    work_in_progress = models.Request.objects.all().filter(customer_id=customer.id, status='Repairing').count()
    work_completed = models.Request.objects.all().filter(customer_id=customer.id).filter(
        Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made = models.Request.objects.all().filter(customer_id=customer.id).filter(
        Q(status="Pending") | Q(status="Approved")).count()
    bill = models.Request.objects.all().filter(customer_id=customer.id).filter(
        Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict = {
        'work_in_progress': work_in_progress,
        'work_completed': work_completed,
        'new_request_made': new_request_made,
        'bill': bill['cost__sum'],
        'customer': customer,
    }
    return render(request, 'vehicle/customer_dashboard.html', context=dict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'vehicle/customer_request.html', {'customer': customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(customer_id=customer.id, status="Pending")
    return render(request, 'vehicle/customer_view_request.html', {'customer': customer, 'enquiries': enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request, pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiry = models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request, 'vehicle/customer_view_approved_request.html',
                  {'customer': customer, 'enquiries': enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request, 'vehicle/customer_view_approved_request_invoice.html',
                  {'customer': customer, 'enquiries': enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiry = forms.RequestForm()
    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        if enquiry.is_valid():
            customer = models.Customer.objects.get(user_id=request.user.id)
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.customer = customer
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request, 'vehicle/customer_add_request.html', {'enquiry': enquiry, 'customer': customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'vehicle/customer_profile.html', {'customer': customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(request.FILES, instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm, 'customer': customer}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request, 'vehicle/edit_customer_profile.html', context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request, 'vehicle/customer_invoice.html', {'customer': customer, 'enquiries': enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    feedback = forms.FeedbackForm()
    if request.method == 'POST':
        feedback = forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request, 'vehicle/feedback_sent_by_customer.html', {'customer': customer})
    return render(request, 'vehicle/customer_feedback.html', {'feedback': feedback, 'customer': customer})

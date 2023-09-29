from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer


def create_customer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        customer = Customer.objects.create(email=email)
        customer.save()
        return redirect('success')
    else:
        return HttpResponse('This is create customer page')
    
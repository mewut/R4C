from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order
from customers.models import Customer
from robots.models import Robot


def create_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        robot_serial = request.POST.get('robot_serial')
        try:
            customer = Customer.objects.get(id=customer_id)
            robot = Robot.objects.get(serial=robot_serial)

            # создаем заказ
            order_instance = Order.objects.create(customer=customer, serial=robot)

            if order_instance:
                return redirect('order_success')
            else:
                return redirect('waiting_list', robot_serial=robot_serial)
        except (Customer.DoesNotExist, Robot.DoesNotExist):
            return HttpResponse('Error creating order')
    else:
        robots = Robot.objects.filter(quantity__gt=0)
        context = {'robots': robots}
        return HttpResponse(context)
    

def waiting_list(robot_serial):
    robot = get_object_or_404(Robot, serial=robot_serial)

    if robot.quantity > 0 and robot.waiting_list.exists():
        customer = robot.waiting_list.first()
        order = Order.objects.create(customer=customer, serial=robot)
        order.save()

        # удаляем клиента из листа ожидания, если роботов стало больше нуля. В сигналах в это время клиенту придет письмо, что робот появился в наличии
        robot.waiting_list.remove(customer)
        robot.save()

        return True
    else:
        return False
    
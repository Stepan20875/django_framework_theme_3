# from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from .models import Employee
from django.contrib.auth.decorators import login_required

def home(request):
    employees = Employee.objects.all()
    return render(request, 'personnel/home.html', {'employees': employees, 'project_description':"Описание проекта"})
    # return render(request, 'personnel/home.html', context)


def employee_list(request):
    employees = Employee.objects.all()  # You might want to change this to a paginated version
    return render(request, 'personnel/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'personnel/employee_detail.html', {'employee': employee})
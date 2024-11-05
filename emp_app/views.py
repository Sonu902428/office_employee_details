from django.shortcuts import render,HttpResponse
from . models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
import csv

# Create your views here.

def index(request):
    return render(request,'index.html')
    
def show_all(request):
    emps = Employee.objects.all()
    context ={
        'emps' : emps
    }
    
    return render(request,'show.html',context)
    

def add_emp(request):
    if request.method=="POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        dept = int(request.POST["dept"])
        role = int(request.POST["role"])
        salary = int(request.POST["salary"])
        bonus = int(request.POST["bonus"])
        phone = int(request.POST["phone"])
    
        new_emp = Employee(firstname=firstname,lastname=lastname,dept_id=dept,role_id=role,salary=salary,bonus=bonus,phone=phone,hire_date=datetime.now())
        print(new_emp)
        new_emp.save()
       
        return HttpResponse("Employee added successful")
    
    elif request.method == "GET":
        return render(request,'add.html')
    else:
        return HttpResponse("Exceptions occured Employee is not added")

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee has been removed successfully...")
        except:
            return HttpResponse("Enter Employee's valid details")


    emps = Employee.objects.all()
    context ={
        'emps':emps
    }
    return render(request,'remove.html',context)

def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(firstname__icontains=name) | Q(lastname__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains= role)

        context = {
            'emps':emps
        }
        return render(request,'show.html',context)
    
    elif request.method == 'GET':
        return render(request,'filter.html')
    
    else:
        return HttpResponse("An Exception Occured...")
    

def download_emp_details(request):
    emps = Employee.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_details.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Department', 'Role', 'Salary', 'Bonus', 'Phone', 'Hire Date'])

    for emp in emps:
        writer.writerow([
            emp.firstname,
            emp.lastname,
            emp.dept.name if emp.dept else 'N/A',
            emp.role.name if emp.role else 'N/A',
            emp.salary,
            emp.bonus,
            emp.phone,
            emp.hire_date.strftime('%Y-%m-%d')  # Format hire date if needed
        ])

    return response
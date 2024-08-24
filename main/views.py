from django.shortcuts import render,redirect
from .models import Task
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required(login_url='log_in')
def home(request):
    data = []  # Initialize an empty list to handle unauthenticated users

    if request.user.is_authenticated:
        user = request.user
        data = Task.objects.filter(Isdelete=False, assigned_to=user)

    return render(request, 'main/home.html', context={'data': data})

def create_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        # Create a new task object
        Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            deadline=deadline,
            assigned_to=request.user
        )
        messages.info(request, ' Hi Your Task is created successfully!')
          # Return a success message or redirect
        return redirect('create_form')

    # If not POST, display the form
    return render(request, 'main/form.html')
def delete(request, id):
    data=Task.objects.get(id=id)
    data.Isdelete=True
    data.save()
    return redirect('home')

def edit(request,id):
    data=Task.objects.get(id=id)
    if request.method == 'POST':
        data=Task.objects.get(id=id)
        data.title=request.POST['title']
        data.description=request.POST['description']
        data.status=request.POST['status']
        data.priority=request.POST['priority']
        data.deadline=request.POST['deadline']
        data.save()

        return redirect('home')
    return render(request,'main/edit.html',{'data':data})
def log_in(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,'username is not yet register')
            return redirect('log_in')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'auth/login.html')

def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password1=request.POST.get('password1')

        try:
            validate_password(password)
            if password==password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'username is already exists!!!!')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'email is already exists!!!!')
                    return redirect('register')
                else:
                    User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    return redirect("log_in")
            else:
                    messages.error(request,'password is not match')
                    return redirect('register')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request,error)
                return redirect('register')
    return render(request,'auth/register.html')
def log_out(request):
    logout(request) 
    return redirect('log_in') 

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important for keeping the user logged in
            return redirect('log_in')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'auth/change_pwd.html', {'form': form})


def recycle(request):
    data = Task.objects.filter(Isdelete=True, assigned_to=request.user)
    return render(request, 'main/recycle.html', context={'data': data})



def restore(request, id):
    data=Task.objects.get(id=id)
    data.Isdelete=False
    data.save()
    return redirect('home')
def search(request):
    finds = []  # Initialize an empty list to handle cases where there's no POST request

    if request.method == 'POST':
        search = request.POST.get('search', '')  # Use get() to avoid KeyError
        finds = Task.objects.filter(title__icontains=search)
        finds=finds.filter(Isdelete=False)

    return render(request, 'main/search.html', {'finds': finds})

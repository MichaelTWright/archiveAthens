from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib import messages 
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import bcrypt

def index(request):
    print("hello from index")
    data_list = Archive.objects.order_by("-created_at").all()
    page = request.GET.get('page', 1)

    paginator = Paginator(data_list, 8)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    try:
        if request.session['user_id']:
            print("im in session")
            context = {
                "logged": 1,
                "user": User.objects.get(id=request.session['user_id']),
                "archive_data": data,
                
                # "archive_data": Archive.objects.order_by("-created_at").filter(title__startswith=request.POST['bird']),
            }
            return render(request, 'archive_app/home.html', context)
        else:
            print("im not in session")
            context = {
                "logged": 0, 
                "archive_data": data,
            }
            return render(request, 'archive_app/home.html', context)
    except:
        print("im not in session")
        context = {
            "logged": 0, 
            "archive_data": data,
        }
        return render(request, 'archive_app/home.html', context)

def register(request):
    # Check if entered info is valid
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/register')
        else:
            email = request.POST['email']
            # Check if a user with this email already exists
            try:
                User.objects.get(email=email)
                messages.error(request, "A user with this email already exists")
                return redirect('/register')
            except:
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                password = bcrypt.hashpw(request.POST['password'].encode(),
                        bcrypt.gensalt())
                # Create a new user
                this_user = User.objects.create(first_name = first_name,
                        last_name = last_name, email = email, password = password.decode('utf-8'))
                request.session['user_id'] = this_user.id
                return redirect('/')
    else:
        return render(request, 'archive_app/register.html')

def login(request):
    email = request.POST['email']
    # Check if the user is registered
    
    try:
        this_user = User.objects.get(email=email)
        print("Name: " + this_user.first_name)
        
        if bcrypt.checkpw(
                request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id'] = this_user.id
            return redirect('/')
        else:
            messages.error(request, "Wrong password")
            return redirect('/')
    except:
        messages.error(request, "Email not found")
        return redirect('/')

def logout(request):
    request.session['user_id'] = None
    return redirect('/')

def archive_create(request):
    try:
        form = Archive.objects.create(title=request.POST['title'], img=request.FILES['img'], audio=request.FILES['audio'], user=User.objects.get(id=request.session['user_id']))
        
        return redirect('/')
    
          
    except:
            messages.error(request, "Upload Error. Try Again")
            return redirect('/')


def favorited(request,id):
    a = Archive.objects.get(id=id)
    u = User.objects.get(id=request.session['user_id'])
    a.favorited_users.add(u)
    context = {
            "count": a.favorited_users.all().count()
        }
    return render(request, "archive_app/likes.html", context)



def favorites(request):
    user= User.objects.get(id=request.session['user_id'])
    myfavs= user.favorite_archives.all()

    context = {
       "user" : user, 
       "myfavs" : myfavs 
    }
    return render(request, 'archive_app/favs.html', context)

def unlike(request,id):
    a = Archive.objects.get(id=id)
    u = User.objects.get(id=request.session['user_id'])
    a.favorited_users.remove(u)
    
    return redirect('/favorites')

def uploads(request,id):
    user = User.objects.get(id=id)
    uploads= user.uploads.all()
    try:
        if request.session['user_id']:
            logUser = User.objects.get(id=request.session['user_id'])
            if int(id) == request.session['user_id']:
                context = {
                    "logged": 1,
                    "user" : user, 
                    "uploads" : uploads, 
                    "logUser" : logUser, 
                }
                return render(request, 'archive_app/uploads.html', context)
            else: 
                context = {
                    "logged": 0,
                    "user" : user, 
                    "uploads" : uploads, 
                    "logUser" : logUser, 
                }
                return render(request, 'archive_app/uploads.html', context)
        else: 
            context = {
                    "logged": 2,
                    "user" : user, 
                    "uploads" : uploads, 
                }
            return render(request, 'archive_app/uploads.html', context)
    except: 
        context = {
                    "logged": 2,
                    "user" : user, 
                    "uploads" : uploads, 
                }
        return render(request, 'archive_app/uploads.html', context)
    

def delete(request,id):
    b = Archive.objects.get(id= id)
    b.delete()
    num = request.session['user_id']
    return redirect('/uploads/{}'.format(num))

def find(request):
    data_list = Archive.objects.filter(title__contains=request.POST['search']).order_by("-created_at").all()
    page = request.GET.get('page', 1)

    paginator = Paginator(data_list, 8)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    try:
        if request.session['user_id']:
            context = {
                        "logged": 1,
                        "archive_data" : data,
                    }
            return render(request, "archive_app/all.html", context)
        else:
            context = {
                        "logged": 0,
                        "archive_data" : data,
                    }
            return render(request, "archive_app/all.html", context)
    except:
        context = {
                        "logged": 0,
                        "archive_data" : data,
                    }
        return render(request, "archive_app/all.html", context)
def like(request):
    context = {
                
            }
    return render(request, "archive_app/likes.html", context)




  
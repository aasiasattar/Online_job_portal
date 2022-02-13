from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
from datetime import date

# Create your views here.

def index(request):
    return render(request, 'index.html')


def admin_login(request):
    error = ""
    if request.method=='POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}
    return render(request, 'admin_login.html',d)

def user_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request,user)
                    error = "no"
                else:
                        error = "yes"
            except:
                error = "yes"

        
    d = {'error':error}

    return render(request, 'user_login.html', d)



def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
       f = request.POST['fname']
       l = request.POST['lname']
       con = request.POST['contact']
       gen = request.POST['gender']
       

       student.user.first_name = f
       student.user.last_name = l
       student.mobile = con

       student.gender = gen
       
       try:
           student.save()
           student.user.save()
           error="no"
       except: 
           error="yes"

        
       try:
           i = request.FILES['img']
           student.image = i
           student.save()
           error="no"
       except: 
           pass
    d = {'student':student,'error':error} 
    return render(request, 'user_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')
    


def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = RecruiterUser.objects.get(user=user)
                if user1.type == "recruiter" and user1.status!="pending":
                    login(request,user)
                    error = "no"
                else:
                        error = "not"
            except:
                error = "yes"

        else:
            error = "yes"
    d = {'error':error}
    return render(request, 'recruiter_login.html',d)









def user_signup(request):
    error = ""
    if request.method == 'POST':
       f =  request.POST['fname']
       l = request.POST['lname']
       con = request.POST['contact']
       e = request.POST['email']
       p = request.POST['pwd']
       gen = request.POST['gender']
       i = request.FILES['img']
       try:
           user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           StudentUser.objects.create(user=user,mobile=con,image=i,gender=gen,type="student") 
           error="no"
       except: 
           error="yes"
    d={'error':error}

    return render(request, 'user_signup.html',d)






def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
       f = request.POST['fname']
       l = request.POST['lname']
       con = request.POST['contact']
       e = request.POST['email']
       p = request.POST['pwd']
       gen = request.POST['gender']
       i = request.FILES['img']
       comp = request.POST['company']
       try:
           user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           RecruiterUser.objects.create(user=user,mobile=con,image=i,gender=gen,company=comp,type="recruiter",status="pending") 
           error="no"
       except: 
           error="yes"
    d={'error':error}

    return render(request,'recruiter_signup.html',d)




def recruiter_home(request):
    if not request.user.is_authenticated:

       return redirect('recruiter_login')

    user = request.user
    recruiter = RecruiterUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
       f = request.POST['fname']
       l = request.POST['lname']
       con = request.POST['contact']
       gen = request.POST['gender']
       comp = request.POST['company']

       recruiter.user.first_name = f
       recruiter.user.last_name = l
       recruiter.mobile = con
       recruiter.company = comp
       recruiter.gender = gen
       
       try:
           recruiter.save()
           recruiter.user.save()
           error="no"
       except: 
           error="yes"

        
       try:
           i = request.FILES['img']
           recruiter.image = i
           recruiter.save()
           error="no"
       except: 
           pass
    d = {'recruiter':recruiter,'error':error}  
    return render(request,'recruiter_home.html',d)





def admin_home(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    rcount = RecruiterUser.objects.all().count()
    scount = StudentUser.objects.all().count()
    return render(request, 'admin_home.html',{'rcount':rcount,'scount':scount})



def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    
    return render(request,'view_users.html',{'data':data})



def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')



def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = RecruiterUser.objects.filter(status='pending')
    
    
    return render(request,'recruiter_pending.html',{'data':data})


def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    recruiter = RecruiterUser.objects.get(id=pid)
    if request.method=="POST":
        s = request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error = "no"
        except:
            error = "yes"

    d = {'recruiter':recruiter,'error':error}
    
    return render(request,'change_status.html',d)



def recruiter_accepted(request):
       if not request.user.is_authenticated:
         return redirect('admin_login')
       data = RecruiterUser.objects.filter(status='Accept')
    
    
       return render(request,'recruiter_accepted.html',{'data':data})


def recruiter_rejected(request):
       if not request.user.is_authenticated:
         return redirect('admin_login')
       data = RecruiterUser.objects.filter(status='Reject')
    
    
       return render(request,'recruiter_rejected.html',{'data':data})



def recruiter_all(request):
       if not request.user.is_authenticated:
         return redirect('admin_login')
       data = RecruiterUser.objects.all()
    
    
       return render(request,'recruiter_all.html',{'data':data})



def recruiter_delete(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')




def change_password_admin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    error = ""
    
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
                
        except:
            error = "yes"

    d = {'error':error}
    
    return render(request,'change_password_admin.html',d)



def change_password_user(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    error = ""
    
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
                
        except:
            error = "yes"

    d = {'error':error}
    
    return render(request,'change_password_user.html',d)





def change_password_recruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""
    
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
                
        except:
            error = "yes"

    d = {'error':error}
    
    return render(request,'change_password_recruiter.html',d)




def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == 'POST':
       jt = request.POST['jobtitle']
       sd = request.POST['startdate']
       ed = request.POST['enddate']
       sal = request.POST['salary']
       l = request.FILES['logo']
       skills = request.POST['skills']
       exp = request.POST['experience']
       loc = request.POST['location']
       des = request.POST['description']
       user=request.user
       recruiter=RecruiterUser.objects.get(user=user)
       try:
           Job.objects.create(recruiter=recruiter,title=jt,start_date=sd,end_date=ed,salary=sal,image=l,skills=skills,experience=exp,location=loc,description=des,creationdate=date.today()) 
           error="no"
       except: 
           error="yes"
    d={'error':error}

    return render(request,'add_job.html',d)




def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = RecruiterUser.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    d={'job':job}
  
    return render(request,'job_list.html',d)





def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)


    if request.method == 'POST':
       jt = request.POST['jobtitle']
       sd = request.POST['startdate']
       ed = request.POST['enddate']
       sal = request.POST['salary']
       skills = request.POST['skills']
       exp = request.POST['experience']
       loc = request.POST['location']
       des = request.POST['description']


       job.title = jt
       job.salary = sal
       job.skills = skills
       job.experience = exp
       job.location = loc
       job.description = des
       

       try:
           job.save() 
           error="no"
       except: 
           error="yes"
       
       
       if sd:
           try:

               job.start_date = sd
               job.save()


           except:
                pass

       else: 
           pass 

       if ed:
           try:

               job.end_date = ed
               job.save


           except:
                pass

       else: 
           pass

    d={'error':error,'job':job}

    return render(request,'edit_jobdetail.html',d)




def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)


    if request.method == 'POST':
       jt = request.POST['jobtitle']
       sd = request.POST['startdate']
       ed = request.POST['enddate']
       sal = request.POST['salary']
       skills = request.POST['skills']
       exp = request.POST['experience']
       loc = request.POST['location']
       des = request.POST['description']


       job.title = jt
       job.salary = sal
       job.skills = skills
       job.experience = exp
       job.location = loc
       job.description = des
       

       try:
           job.save() 
           error="no"
       except: 
           error="yes"
       
       
       if sd:
           try:

               job.start_date = sd
               job.save()


           except:
                pass

       else: 
           pass 

       if ed:
           try:

               job.end_date = ed
               job.save


           except:
                pass

       else: 
           pass

    d={'error':error,'job':job}

    return render(request,'edit_jobdetail.html',d)






def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)


    if request.method == 'POST':
       lo = request.FILES['logo']
       job.image = lo
       try:
           job.save() 
           error="no"
       except: 
           error="yes"
       
    d={'error':error,'job':job}

    return render(request,'change_companylogo.html',d)




def latest_jobs(request):
    job = Job.objects.all().order_by('-creationdate')
    return render(request,'latest_jobs.html',{'job':job})




def user_latestjobs(request):
    job = Job.objects.all().order_by('-creationdate')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    li = []
    for i in data:
        li.append(i.job.id)

    return render(request,'user_latestjobs.html',{'job':job,'li':li})



def job_detail(request,pid):
    job = Job.objects.get(id=pid)
    return render(request,'job_detail.html',{'job':job,})






def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()
    if job.end_date < date1:
        error = "close"
    elif job.start_date > date1:
        error = "notopen"
    else:

        if request.method == 'POST':
         r= request.FILES['resume']
         Apply.objects.create(student=student,job=job,resume=r,applydate=date.today())
         error = "success"

       
    d={'error':error}

    return render(request,'applyforjob.html',d)





def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data = Apply.objects.all()
    d={'data':data}

    return render(request,'applied_candidatelist.html',d)



def contact(request):
    return render(request,'contact.html')






























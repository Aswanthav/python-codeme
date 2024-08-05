from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Blog,Comment,Profile,UserOTP
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .form import *
import random
from django.core.mail import send_mail
from django.views.generic import ListView,CreateView,UpdateView,DetailView,ListView
from .models import *
from django.urls import reverse_lazy,reverse
import random

# Create your views here. 


# def codeme(request):
#     return HttpResponse("welcome")


def self(request):
    return render(request,"demo.html")


def demo1(request):
    context= {"name":"junid"}
    return render(request,"demo1.html",context)
 


def demo2(request):
    context = {"name":{"aswanth","junid","rajeer"}}
    return render(request,"demo2.html",context)


def demo3(request):
    data = [
        {'name' : 'aswanth' , 'age' : '20' ,'place' : 'vadakara'},
        {'name' : 'junid' , 'age' : '21' ,'place' : 'malappuram'},
        {'name' : 'rajeer' , 'age' : '22' ,'place' : 'kannur'}
    ]
    context = { 'student' : data }
    return render(request,"demo3.html",context)


@login_required(login_url="login")
def home(request):
    blog = Blog.objects.filter(is_published=True)
    if request.method == "POST":
        search=request.POST.get("search")
        blog= Blog.objects.filter(title__icontains = search) 
    context = {'blog':blog}
    return render(request,"home.html",context)


@login_required(login_url="login")
def blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        con = request.POST.get('con')
        image = request.FILES.get('image')
        cate = request.POST.get('cate')
        blog = Blog.objects.create(title=title,context=con,image=image,category=cate,fk_user=request.user)
        blog.save()
        messages.success(request,"blog creat succefully!")
        return redirect('home')
    messages.error(request,"password doesn't match... please try agin")
    context= {'cat':Blog.cat_choice}
    return render(request,"blog_create.html",context)


@login_required(login_url="login")
def details(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog=None
    blog_de = Blog.objects.get(id=id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(comment=comment,fk_user = request.user,fk_blog= blog_de)
        messages.success(request,"comment posted succefully!")
    messages.error(request,'comment posted error..')
    comments = Comment.objects.filter(fk_blog=blog_de)
    context= {"blog":blog_de,'comments':comments}
    return render(request,"details.html",context)

@login_required(login_url="login")
def edit(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog=None
    if request.user != blog.fk_user:
        return HttpResponse('sorry permission is denied!')
    # blog=Blog.objects.get(id=id)
    if request.method == 'POST':
        title=request.POST.get('title')
        context=request.POST.get('context')
        image = request.FILES.get('image')
        cate = request.POST.get('cate')
        if title:
            blog.title=title
        if context:
            blog.context=context
        if image:
            blog.image=image
        if cate:
            blog.category=cate
        blog.fk_user=request.user
        blog.save()
        messages.success(request,"blog create succefully!")
        return redirect('details',blog.id)
    # messages.error(request,"password doesn't match... please try agin")
    context ={'blog':blog,'cat':Blog.cat_choice}
    return render(request,"edit.html",context)


@login_required(login_url="login")
def blog_delete(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog=None
    if request.user != blog.fk_user:
        return HttpResponse('sorry permission is denied!')
    blog= Blog.objects.get(id=id)
    if request.method=='POST':
        blog.delete()
        messages.success(request,"blog creat succefully!")
        return redirect('home')
    messages.error(request,"password doesn't match... please try agin")
    context={'blog':blog}
    return render(request,'blog_delete.html',context)



def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user=User.objects.create_user(username=username,email=email,password=password2)
            user.save()
            messages.success(request,"Registration Successfully!")
            return redirect('login')
        messages.error(request,"Password doesn't match... please try again....")
    return render(request,"register.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            if user.is_superuser:
                messages.success(request,"successfuly logged !")
                return redirect('admin_home')
            elif Profile.objects.filter(name=user).exists():
                return redirect('home')
            else:
                messages.success(request,"successfuly logged !")
                return redirect('user_profile')
        messages.error(request,"Password doesn't match... please try again....")
        return redirect('register')
    return render(request,"login_user.html")
        

def user_logout(request):
    logout(request)
    messages.success(request,"successfuly logout !")
    return redirect('login')


@login_required(login_url="login")
def comment_edit(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog=None
    if request.user != comment.fk_user:
        return HttpResponse('sorry permission is denied!')
    comment=Comment.objects.get(id=id)
    blog=comment.fk_blog
    comments=Comment.objects.filter(fk_blog=blog)
    if request.method=='POST':
        edited_comment=request.POST.get('comment')
        comment.comment=edited_comment
        comment.save()
        return redirect('details',blog.id)
    context={'comment':comment,'blog':blog,'comments':comments}
    return render(request,"details.html",context)


@login_required(login_url="login")
def comment_delete(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog=None
    if request.user != comment.fk_user:
        return HttpResponse('sorry permission is denied!')
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect("details",comment.fk_blog.id)


@login_required(login_url="login")
def admin_home(request):
    if not request.user.is_superuser:
        return HttpResponse("permission is Denied")
    try:
        blog=Blog.objects.all()
    except:
        blog=None
    context={'blog':blog}
    return render(request,"admin_home.html",context)



@login_required(login_url="login")
def change_status(request,id):
    if not request.user.is_superuser:
        return HttpResponse("permission is Denied")
    try:
        blog=Blog.objects.get(id=id)
    except:
        blog=None
    blog.is_published= not blog.is_published
    blog.save()
    messages.success(request,"status changed")
    return redirect("admin_home")


def user_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        print("name",name)
        address = request.POST.get('address')
        print("address",address)
        phone = request.POST.get('phone')
        print("phone",phone)
        email = request.POST.get('email')
        print("email",email)
        gender = request.POST.get('gender')
        print("gender",gender)
        image = request.FILES.get('image')
        print("image",image)
        date_of_birth = request.POST.get('date_of_birth')
        print("date_of_birth",date_of_birth)
        profile = Profile.objects.create(name=request.user,address=address,phone=phone,email=email,gender=gender,image=image,date_of_birth=date_of_birth)
        profile.save()
        return redirect('home')
    return render(request,"user_profile.html")



def user_detail(request,id):
    Profile = get_object_or_404(User,id=id)
    context={'profile':Profile}
    return render(request,"user_detail.html",context)


def create_new(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.fk_user = request.user
            blog.save()
            messages.success(request,"blog cteated successfully")
            return redirect('home')
        messages.error(request,form.error)
    context={"form":form}
    return render(request,"create_new.html",context)



def blog_edit_new(request,id):
    blog = Blog.objects.get(id=id)
    form = BlogForm(instance=blog)
    if request.method == "POST":
        form= BlogForm(request.POST,request.FILES,instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.fk_user = request.user
            blog.save()
            messages.success(request,'Blog Update Successfully')
            return redirect("details",id)
        messages.error(request,form.error)
    context={"form":form}
    return render(request,"blog_edit_new.html",context)



def forgot(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.filter(username=username).first()
        if user:
            otp = random.randrange(1000,9999)
            email = user.email
            subject = "OTP varifications"
            message = f"this is yoir one time password {otp}"
            from_email = "aswanthav143@gmail.com"
            to = [email]
            send_mail(
                subject = subject,
                message = message,
                from_email = from_email,
                recipient_list = to,
                fail_silently = False
            )
            UserOTP.objects.update_or_create(fk_user=user,defaults={'otp':otp})
            messages.success(request,"OTP send successfully!")
            return redirect("otp_varify",user.id)
        messages.error(request,"user not found please register")
        return redirect("register")
    return render(request,"forgot.html")


def otp_varify(request,id):
    user = User.objects.filter(id=id).first()
    user_obj = UserOTP.objects.filter(fk_user=user).first()
    send_otp = user_obj.otp
    if request.method == "POST":
        submitted_otp  = request.POST.get("otp")
        if submitted_otp == send_otp:
            messages.success(request,"OTP verified successfully")
            return redirect("password_reset",id)
        messages.error(request,"OTP verification feild! please try again..")
    return render(request,"otp_varify.html")
    

def password_reset(request,id):
    user = User.objects.filter(id=id).first() 
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            user.set_password(password2)
            user.save()
            messages.success(request,"password Reset succssfully")
            return redirect("login")
        messages.error(request,"password mismatched,please re-enter")
    return render(request,"password_reset.html")



class SampleCreate(CreateView):
    model = Sample
    template_name = 'aswanth.html'
    form_class = SampleFrom
    success_url = reverse_lazy('home')

class SampleUpdate(UpdateView):
    model = Sample
    template_name = 'aswanth.edit.html'
    form_class = SampleFrom
    success_url = reverse_lazy('sam_detail')
    def get_success_url(self):
        return reverse('sam_detail', kwargs={'pk': self.object.pk})

class SampleList(ListView):
    model = Sample
    template_name = 'sample_home.html'
    context_object_name = 'sam_obj'

class SampleDetail(DetailView):
    model = Sample
    template_name = 'sample_detail.html'
    context_object_name = 'sam'




def codeme_image(request):
    return render(request,"codeme_image.html")

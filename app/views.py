from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, PasswordSetForm, BlogForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.views import PasswordResetConfirmView
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .task import send_blog_mail_celery_task

class IndexView(View):
    template_name = "app/index1.html"

    def get(self, request):
        context = {}
        context['blogs_obj'] = Blog.objects.all().order_by('-id')
        # context['search'] = Blog.objects.all()
        context['comment_obj'] = BlogComment.objects.all()
        return render(request, self.template_name, context)

    def post(self, request):
        pass


class RegisterView(View):
    template_name = "app/register.html"

    def get(self, request):
        if not request.user.is_authenticated:
            context = {}
            form = UserRegisterForm()
            context['form'] = form
            return render(self.request, self.template_name, context)
        return HttpResponseRedirect(reverse('index'))

    def post(self, request):
        form = UserRegisterForm(request.POST, request.FILES )
        context = {}
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            confirm_password = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email is already exist in the sytem!")
                context['form'] = form
                return render(request, self.template_name, context)
            if password == confirm_password:
                form.save()
                messages.success(request, "Account create successfully")
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request, "Confirm Passwrd didn't match!!")
                context['form'] = form
                return render(request, self.template_name, context)
        else:
            messages.error(request, "Please enter the valid data!!")
            context['form'] = form
            return render(request, self.template_name, context)


class LoginView(View):
    template_name = "app/login.html"

    def get(self, request):
        context = {}
        if not request.user.is_authenticated:
            form = AuthenticationForm()
            context['form'] = form
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse("index"))

    def post(self, request):
        context = {}
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, f"User login successfully!")
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, "Invalid username and password wrong")
                context['form'] = form
                return render(request, self.template_name, context)
                # return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Invalid username and password wrong")
            context['form'] = form
            return render(request, self.template_name, context)
            # return HttpResponseRedirect(reverse("login"))


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Logout successfully!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "You are not logout")
            return HttpResponseRedirect(reverse("login"))
        


class Forgot_password(View):
    template_name = "app/forgot-password.html"
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)   
            uid=urlsafe_base64_encode(force_bytes(user.id))    
            reset_link = request.build_absolute_uri('/change_password/' + uid + '/' + token + '/')
       
            subject = 'forgot_password'
            message = 'hello'
            data = send_mail(
                subject,
                'Click the following link to reset your password: ' + reset_link,
                settings.EMAIL_HOST_USER,
                ['ranjeet.studio45@gmail.com',],
                fail_silently=False,
                )
            messages.success(request, "Please check you email notification and chenge Password!")
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "User not found!")
            return HttpResponseRedirect(reverse("forgot_password"))  
        

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'app/change-password.html'
    form_class = PasswordSetForm        

def password_reset_complete(request):
    return render(request, "app/completed-reset-pass.html")


class UserBlogPostView(View):
    template_name = "app/blog.html"
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            form = BlogForm()
            context['form'] = form
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse("index"))
               
    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        # print(request.FILES.get('image'))
        if form.is_valid():
            try:
                blog = form.save(commit=False)
                blog.image = request.FILES.get('image')
                blog.save()
                for img in images:
                    # file_path = default_storage.save('blog_images/' + img.name, ContentFile(img.read()))
                    BlogImage.objects.create(blog=blog, image=img)
                messages.success(request,"blog post seccessfully")
                return HttpResponseRedirect(reverse('index')) 
            except Exception as Error:
                messages.error(request,f"Exception Error: {Error}")
                print(f"Error in Blog post method {Error} - for : {request.user.email}")
                return redirect('add_new_blog')
        else:
            messages.error(request,"blog not post successfully!!")
            return HttpResponseRedirect(reverse('add_new_blog'))  
  

@login_required(login_url="/login/")
def blog_comment(request):
    try:
        if request.method == "POST":
            comment = request.POST.get("comment", None)
            blog_id = request.POST.get("blog_id", None)
            if comment is not None and blog_id is not None:
                blog_obj = Blog.objects.get(pk=blog_id)
                comment_create_obj = BlogComment.objects.create(user=request.user, blog=blog_obj, comment=comment)
                return JsonResponse({"message": "Success",}, status=201)
        return JsonResponse({"message": "Failed"}, status=200)

    except Exception as Error:
        print(f"Error in Blog_comment function: {Error}")
        return JsonResponse({"message": "Failed"}, status=400)
                
class BlogDetailView(View):
    template_name = "app/blog-detail.html"

    def get(self, request, blog_id):
        context = {}
        obj = Blog.objects.get(pk=blog_id)
        context['blog'] = obj
        return render(request, self.template_name, context)


class UserProfile(View):
    template_name = "app/user-profile.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        current_user_obj = request.user
        form = UserRegisterForm(request.POST or None, request.FILES, instance=current_user_obj)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        image = request.FILES.get('image', None)
        if first_name and last_name:
            current_user_obj.first_name = first_name
            current_user_obj.last_name = last_name
            if image != None:
                current_user_obj.image = image
            current_user_obj.save()    
            messages.success(request, 'Profile updated successfully.')
            return HttpResponseRedirect(reverse('index')) 
        else:
            messages.error(request, 'Error updating profile.')
        return HttpResponseRedirect(reverse('user_profile'))

class BlogUpdate(View):
    template_name = "app/blog_update.html" 

    def get(self, request, id):
        context = {}
        context['blogs_obj'] = Blog.objects.get(pk=id)
        return render(request, self.template_name,context)
    
    def post(self, request, id):
        obj=Blog.objects.get(id=id)
        form = BlogForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"blog update seccessfully")
            return HttpResponseRedirect(reverse('index')) 
        else:
            messages.error(request,"blog not updated ")   
            return HttpResponseRedirect(reverse('blog_update',args={id}))
            
    
class BlogDelete(View):
    def get(self, request,id):
        obj = Blog.objects.get(id=id)
        if obj:
            obj.delete()
            messages.success(request,"Blog delete successfully!")
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.success(request,"Blog not delete ")
            return HttpResponseRedirect(reverse('index'))
    
   
class SearchView(View):
    template_name = "app/search.html"  

    def post(self,request):
        context = {}
        query = request.POST['q']
        context ['blogs_obj'] = Blog.objects.filter(title__icontains=query).all() #| Blog.objects.filter(description__icontains=query)
        return render(request, self.template_name, context)   
  
class ShareBlog(View):
    def post(self, request):
        data = request.POST # this is post request data
        name = data.get('name')
        email = data.get('email')
        currentUrl = data.get('currentUrl')  
        send_blog_mail_celery_task.apply_async(args=[name,email,currentUrl])
        return JsonResponse({'status':True, 'msg':'email successfully sent!'})
        










      
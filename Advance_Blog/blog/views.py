from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,HttpResponse,redirect
from .models import Post,Comment,Category
from .forms import CommentForm,PostForm,NewUserForm
from django.views.generic import DeleteView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.text import slugify


def login_signup(request):
    return render(request,"blog/login_signup.html",{})



def signup_page(request):
    form=NewUserForm()
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('blog-index',kwargs={"auth_id":user.id}))
        messages.error(request,"Unsuccessful SignUp : Invalid Information")
    return render(request, "blog/signup.html", {"form": form, "title": "SIGN UP"})



def login_page(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return HttpResponseRedirect(reverse('blog-index',kwargs={"auth_id":user.id}))
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="blog/login.html", context={"login_form":form})




@login_required
def logout_page(request):
    logout(request)
    return redirect('blog/login-signup')


@login_required
def blog_index(request,auth_id):
    posts=Post.objects.all().order_by("-created_on").select_related('authen')
    context={
        "posts":posts,
        "auth_id":auth_id,
    }
    return render(request,"blog/index.html",context)





def blog_category(request,category):
    posts=Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context={
        "posts":posts,
        "category":category,
    }
    return render(request,"blog/category.html",context)



@login_required
def blog_detail(request,slug,post_id,auth_id):
    post=Post.objects.get(pk=post_id)
    author_i=User.objects.get(pk=auth_id)                   #changes
    form=CommentForm()
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    
    comments=Comment.objects.filter(post=post)
    context={
        "authori":author_i,
        "post":post,
        "comments":comments,
        "form":form,
        "auth_id":auth_id,
    }
    return render(request,"blog/detail.html",context)


@login_required
def create_post(request,auth_id):
    category1=Category.objects.get(pk=3)
    auther=User.objects.get(id=auth_id)
    form=PostForm()
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=Post(                                      #change removed author
                title=form.cleaned_data["title"],
                body=form.cleaned_data["body"],
                authen=auther,
                slug=slugify(form.cleaned_data["title"]),
                image=form.cleaned_data["image"],
            )
            
            post.save()
            post.categories.add(category1)
            return HttpResponseRedirect(request.path_info)
    context={
        "form":form,
        "categories":category1,
        "auth_id":auth_id,
    }
    return render(request,'blog/create_post.html',context)



def blog_delete(request,auth_id,post_id):
    post=get_object_or_404(Post,pk=post_id)
    authen1=User.objects.get(pk=auth_id)
    
    if request.method=="POST":
        if post.authen.id==authen1.id:
            post.delete()
            return HttpResponseRedirect(reverse('blog-index',kwargs={"auth_id":auth_id}))
        else:
            messages.error(request,"Not Your Blog")
        
    return render(request,'blog/post_confirm_delete.html',{"post":post,"auth_id":auth_id,"post_id":post_id})     


@login_required
def show_profile(request,auth_id):
    user=User.objects.get(pk=auth_id)
    posts=Post.objects.filter(authen=user)
    context={
        "user":user,
        "posts":posts,
    }
    return render(request,'blog/profile.html',context)

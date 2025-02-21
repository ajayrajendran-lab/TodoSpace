from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.forms import SignUpForm,SignInForm,TodoForm
from django.contrib.auth import authenticate,login,logout
from myapp.models import Todo
from django.db.models import Count
from django.utils.decorators import method_decorator
from myapp.decorators import signin_required
from django.contrib import messages

# Create your views here.
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form_instance=SignUpForm()
        return render(request,"sign_up.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        form_data = request.POST 
        form_instance = SignUpForm(form_data)

        if form_instance.is_valid():
            form_instance.save()
            print("===Account Created===")
            messages.success(request,"Account created successfully")
            return redirect("signin")

        else:
            print("===Account Not Created===")
            messages.error(request,"Account not created")
            return render(request,"sign_up.html",{"form":form_instance})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form_instance = SignInForm()
        return render(request,"sign_in.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        form_data = request.POST
        form_instance = SignInForm(form_data)

        if form_instance.is_valid():
            data = form_instance.cleaned_data
            uname = data.get("username")
            pwd = data.get("password")
            user_object = authenticate(request,username=uname,password=pwd)

            if user_object:
                print("===Sign in success===")
                login(request,user_object)
                print("==session started===")
                print(request.user)
                return redirect("todo-add")

            else:
                print("Sign in failed")
                return render(request,"sign_in.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class IndexView(View):

    def get(self,request,*args,**kwargs):

        category_summary=Todo.objects.filter(owner=request.user).values("category").annotate(count=Count("category"))

        priority_summary=Todo.objects.filter(owner=request.user).values("priority").annotate(count=Count("priority"))

        status_summary=Todo.objects.filter(owner=request.user).values("status").annotate(count=Count("status"))
        print(category_summary)
        print(priority_summary)
        print(status_summary)


        # context ={
        #     "category_dict":{cat.get("category"):cat.get("category__count") for cat in category_summary},
        #     "priority_dict":{p.get("priority"):p.get("priority__count") for p in priority_summary},
        #     "status_dict":{stat.get("status"):stat.get("status__count") for stat in status_summary}
        # }
        # context.update(category_dict)
        # context.update(priority_dict)
        # print(context)
        context = {
            "category_summary":category_summary,
            "priority_summary":priority_summary,
            "status_summary":status_summary
        }

        return render(request,"index.html",context)

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        print("===session ended===")
        messages.success(request,"Signout successful")
        return redirect("home")

@method_decorator(signin_required,name="dispatch")
class TodoCreateView(View):

    def get(self,request,*args,**kwargs):
        form_instance = TodoForm()
        return render(request,"todo_add.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        form_data = request.POST 
        form_instance = TodoForm(form_data)

        if form_instance.is_valid():
            data=form_instance.cleaned_data
            Todo.objects.create(**data,owner=request.user)
            print("Task added")
            messages.success(request,"Task added successfully")
            return redirect("todo-add")

        else:
            print("===Task Not added==")
            messages.error(request,"Task not added")
            return render(request,"todo_add.html",{"form_instance"})

@method_decorator(signin_required,name="dispatch")
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        Todo.objects.get(id=id).delete()
        print("Task deleted")
        messages.success(request,"Task deleted successfully")
        return redirect("todo-add")

@method_decorator(signin_required,name="dispatch")
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        form_instance = TodoForm(instance=qs)
        return render(request,"todo_edit.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        form_data = request.POST
        form_instance = TodoForm(form_data,instance=qs)

        if form_instance.is_valid():
            form_instance.save()
            print("Todo Updated")
            messages.success(request,"Task updated successfully")
            return redirect("todo-all")
        else:
            print("Todo not updated")
            messages.error(request,"Task not updated")
            return render(request,"todo_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(owner=request.user).order_by("created_at")
        return render(request,"todo_list.html",{"data":qs})

class HomeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"home.html")
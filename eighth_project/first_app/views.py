from django.shortcuts import render, redirect
from .forms import RegisterForm, ChangeUserData
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic import ListView,DetailView
from .models import Car, Brand,Comment, Order
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.

def home(request):
    brand_name = request.GET.get('brand')
    cars = Car.objects.all() 


    if brand_name:
        cars = cars.filter(brand__name=brand_name)

    brands = Brand.objects.all()

    return render(request, 'home.html', {'cars': cars,'brands': brands,})
    
    
    
    
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                messages.success(request,'Acoount Created Successfully')
                form.save()
                print(form.cleaned_data)
        else:
            form=RegisterForm()
        return render(request,'./signup.html',{'form':form})
    else:
        return redirect('profile')

    
class UserLoginView(LoginView):
    template_name='signup.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    
    
    def form_valid(self, form):
        messages.success(self.request,'Loged In Successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,'Please Enter Valid Information')
        return super().form_valid(form)
        
        


def profile(request):
    if  request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangeUserData(request.POST,instance=request.user)
            if form.is_valid():
                messages.success(request,'Acoount Updated Successfully')
                form.save()
                print(form.cleaned_data)
        else:
            form=ChangeUserData(instance=request.user)
        return render(request,'./profile.html',{'form':form})
    else:
        return redirect('login')


def user_logout(request):
    logout(request)
    return redirect('login')
        


def pass_change(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PasswordChangeForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                return redirect('profile')
        else:
            form=PasswordChangeForm(user=request.user)
        return render(request,'./passchange.html',{'form':form})
    else:
        return redirect('login')


def pass_change2(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=SetPasswordForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                return redirect('profile')
        else:
            form=SetPasswordForm(user=request.user)
        return render(request,'./passchange.html',{'form':form})
    else:
        return redirect('login')
    
    
def change_user_data(request):
    if  request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangeUserData(request.POST,instance=request.user)
            if form.is_valid():
                messages.success(request,'Acoount Updated Successfully')
                form.save()
                print(form.cleaned_data)
        else:
            form=ChangeUserData()
        return render(request,'./profile.html',{'form':form})
    else:
        return redirect('login')





class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'  
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_name = self.request.GET.get('brand')
        if brand_name:
            queryset = queryset.filter(brand__name=brand_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()  # Get all brands for the filter
        return context




class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            car = self.get_object()
            if car.quantity > 0:
                Order.objects.create(user=request.user, car=car)
                car.quantity -= 1
                car.save()
            return redirect('profile')
        return redirect('login')
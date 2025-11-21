from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import regform
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from .models import Products,CartItem
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import ListView
# Create your views here.

class register(View):
    def get(self,request,*args,**kwargs):
        form=regform()
        return render(request,'register.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form=regform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

class login_view(View):
    def get(self,request,*args, **kwargs):
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})
    
    def post(self,request,*args, **kwargs):
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('login')

def base(request):
    return render(request,'base.html')

def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        product=Products.objects.filter(Q(p_category__icontains=q) | Q(p_title__icontains=q))
        context={'products': product}
        return render(request,'search.html',context)
    return render(request,'home.html')

class keyboards_view(ListView):
    model = Products
    template_name = 'keyboards.html'
    context_object_name = 'keyboard'

    def get_queryset(self):
        return Products.objects.filter(p_category__icontains='keyboard')
    
class graphiccards_view(ListView):
    model = Products
    template_name = 'graphiccards.html'
    context_object_name = 'gpus'

    def get_queryset(self):
        return Products.objects.filter(p_category__icontains='graphic card')

class huddies_view(ListView):
    model = Products
    template_name = 'huddies.html'
    context_object_name = 'huddies'

    def get_queryset(self):
        return Products.objects.filter(p_category__icontains='huddie')

class leds_view(ListView):
    model = Products
    template_name = 'leds.html'
    context_object_name = 'leds'
    
    def get_queryset(self):
        return Products.objects.filter(p_category__icontains='LED')
    

class detail_view(View):
    def get(self,request,pk,*args, **kwargs):
        product=get_object_or_404(Products,pk=pk)
        return render(request,'detail.html',{'product':product})

    def post(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        product=get_object_or_404(Products,pk=pk)
        size=request.POST.get('size')
        color=request.POST.get('color')
        try:
          items= CartItem.objects.get(user=request.user,product=product)
        except CartItem.DoesNotExist:
            items=CartItem.objects.create(user=request.user,product=product,size=size,color=color,quantity=1)
        items.save()
        return redirect('cart')
    
@login_required(login_url='login')
def add_to_cart(request,item_id):
    product=get_object_or_404(Products,id=item_id)  
    try:
        c_item=CartItem.objects.get(user=request.user,product=product)
    except CartItem.DoesNotExist:
        c_item=CartItem.objects.create(user=request.user,product=product,quantity=1)
    c_item.save()
    return redirect('cart')

def cart(request):
    c_item=CartItem.objects.filter(user=request.user)
    total=sum(item.total() for item in c_item)
    return render (request,'addtocart.html',{'c_item':c_item,'total':total})

def increase_item(request,item_id):
    c_item=get_object_or_404(CartItem,user=request.user,id=item_id)
    c_item.quantity +=1
    c_item.save()
    return redirect('cart')

def decrease_item(request,item_id):
    c_item=get_object_or_404(CartItem,user=request.user,id=item_id)
    if c_item.quantity >1:
        c_item.quantity -=1
        c_item.save()
    return redirect('cart')

def remove_item(request,item_id):
    c_item=get_object_or_404(CartItem,user=request.user,id=item_id)
    c_item.delete()
    return redirect('cart')

def checkout(request):
    product=CartItem.objects.filter(user=request.user)
    total=sum(item.total() for item in product)
    return render(request,'checkout.html',{'item':product,'total':total})

def success_view(request):
    return render(request,'success.html')
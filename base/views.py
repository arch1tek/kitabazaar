from csv import excel
from itertools import product
from re import template
from decimal import Decimal as D
from unicodedata import name
from django.db.models import Max
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from django.forms import ModelForm, Form, modelformset_factory
from django.template.context_processors import csrf
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin



from .models import *
# Create your views here.
def homePage(request):
    productslist=Product.objects.filter(sold=False)
    branchlist=Branch.objects.all()
    courselist=Course.objects.all()
    filter_course=None
    show_course=None
    filter_bookname=None
    show_bookname=''
    filter_author=None
    show_author=''
    filter_price1=None
    showprice1=None
    filter_price2=None
    showprice2=None
    print(request)
    if request.method=='GET':
        if 'min_price' in request.GET:
            filter_price1 = request.GET['min_price']
            showprice1=filter_price1
            if filter_price1=='':
                showprice1=None
                filter_price1=0
        if 'max_price' in request.GET:
            filter_price2 = request.GET['max_price']
            showprice2=filter_price2
            if filter_price2=='':
                showprice2=None
                filter_price2=productslist.aggregate(Max('price'))
                filter_price2=filter_price2['price__max']
        print (filter_price1)
        print (filter_price2)
        productslist=productslist.filter(price__range=(filter_price1,filter_price2))
        
        if 'branch' in request.GET:
            if request.GET['branch']!=None:
                filterbranch=request.GET['branch']
                print(filterbranch)
                
                if filterbranch=='':
                    productslist=productslist
                else:
                    productslist=productslist.filter(bookID__belongstocourse__branch__branchName=filterbranch)
                    courselist=courselist.filter(branch=filterbranch)
                    
        if 'course' in request.GET:
            if request.GET['course']!=None:
                filter_course=request.GET['course']
                
                if filter_course=='':
                    productslist=productslist
                else:
                    productslist=productslist.filter(bookID__belongstocourse__courseID=filter_course)
        
        if 'bookname' in request.GET:
            if request.GET['bookname']!=None:
                filter_bookname=request.GET['bookname']
                
                if filter_bookname=='':
                    productslist=productslist
                    show_bookname=''
                else:
                    show_bookname=filter_bookname
                    productslist=productslist.filter(bookID__bookName__contains=filter_bookname)
        if 'author' in request.GET:
            if request.GET['author']!=None:
                filter_author=request.GET['author']
                
                if filter_author=='':
                    productslist=productslist
                    show_author=''
                else:
                    show_author=filter_author
                    productslist=productslist.filter(bookID__writtenby__authorName__contains=filter_author)

    else:
        message = 'You submitted nothing!'
    


    args={}
    args.update(csrf(request))
    args['productslist']=productslist
    args['showprice1']=showprice1
    args['showprice2']=showprice2
    args['branchlist']=branchlist
    args['courselist']=courselist
    args['show_bookname']=show_bookname
    args['show_author']=show_author
    print(args)
    return render(request, "base/home.html", args)

class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self) -> str:
        return reverse_lazy('home')

class ProductDetails(LoginRequiredMixin, ModelForm):
    
    class Meta:
        model = Product
        exclude = ['sellerID','sold']

    def form_valid(self, form):
        print(self.request.user)
        form.instance.sellerID = Profile.objects.get(user=self.request.user)
        return super(ProductDetails, self).form_valid(form)
    
    '''def get(self, *args, **kwargs):
        return super(ProductDetails, self).get(*args, **kwargs)'''

class UploadProductPhotos(ModelForm):
    class Meta:
        model=ProductPhotos
        exclude=['productID']
        


def enlistProduct(request):

    ImageFormSet = modelformset_factory(ProductPhotos,
                                        form=UploadProductPhotos, extra=3)

    if request.method=="POST":
        productform=ProductDetails(request.POST)
        photoform=ImageFormSet(request.POST, request.FILES,queryset=ProductPhotos.objects.none())

        
        if all((productform.is_valid(), photoform.is_valid())):
            print('ded')
            
            prod = productform.save(commit=False)
            prod.sellerID=Profile.objects.get(user=request.user)
            prod.save()
            for form in photoform.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['photo']
                    photo = ProductPhotos(productID=prod, photo=image)
                    photo.save()
            return redirect('home')
    else:
        productform=ProductDetails()
        photoform=ImageFormSet(queryset=ProductPhotos.objects.none())


    args={}
    args.update(csrf(request))
    args['photoform']=photoform
    args['productform']= productform
    return render(request, "base/enlist.html", args)


class RegisterView(UserCreationForm):

    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterView, self).get(*args, **kwargs)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'wallet']

def newUser(request):
    if request.method=="POST":
        register_view_form=RegisterView(request.POST)
        profile_form=ProfileForm(request.POST)

        if all((profile_form.is_valid(), register_view_form.is_valid())):
            reg = register_view_form.save()
            profile = profile_form.save(commit=False)
            profile.user = reg
            profile.save()
            return redirect('home')

    else:
        register_view_form=RegisterView()
        profile_form=ProfileForm()

    args={}
    args.update(csrf(request))
    args['register_view_form']=register_view_form
    args['profile_form']= profile_form


    return render(request, "base/register.html", args)

class ProductDetailsbuy(LoginRequiredMixin,DetailView):
    model= Product
    context_object_name = 'product'
    template_name = 'base/productdetails.html'

    def get_photos(self):
        print(self.get_context_data)
        return self.args
    
class Transactionform(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['productID','buyerID','time']

def buyproduct(request, **kwargs):
    product=Product.objects.get(id=kwargs['pk'])
    if request.method=="POST":
        
        transaction=Transactionform(request.POST)

        print('ded')
        transaction = transaction.save(commit=False)
        transaction.buyerID=Profile.objects.get(user=request.user)
        transaction.productID=product
        transaction.save()
        product.sold=True
        product.save()
        Profile.objects.filter(user=request.user).update(wallet=Profile.objects.get(user=request.user).wallet-product.price)
        Profile.objects.filter(user=product.sellerID).update(wallet=Profile.objects.get(user=product.sellerID).wallet+product.price)
        return redirect('home')
    else:
        
        transaction=Transactionform()
        
    args={}
    args.update(csrf(request))
    args['product']=product
    args['transaction']= transaction


    return render(request, "base/productdetails.html", args)


class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('myproducts')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(sellerID=Profile.objects.get(user=owner))

def myProducts(request):
    myproductslist=Product.objects.filter(sellerID=Profile.objects.get(user=request.user))
    args={}
    args.update(csrf(request))
    args['myproductslist']=myproductslist
    
    return render(request, "base/myproducts.html", args)

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['conditionofbook', 'price', 'bookID']
    success_url = reverse_lazy('myproducts')
    
    
class CreateBook(CreateView):
    model = Book
    fields='__all__'
    
class CreateAuthor(CreateView):
    model = Author
    fields='__all__'
    
class CreateCourse(CreateView):
    model = Course
    fields='__all__'
    
def ProfileView(request):
    profile=Profile.objects.get(user=request.user)
    args={}
    args.update(csrf(request))
    args['profile']=profile
    return render(request, "base/profiledetails.html", args)
    
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import ContentForm, BrandForm, CreateUserForm
from django.views.generic import DetailView
from .filters import ContentFilter, BrandFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def registerPage(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account is done Mr.{username}, Thanks you')
                return redirect('/')
        else:
            form = CreateUserForm()
        context = {
            'form': form,
        }
        return render(request, 'account/register.html', context)
    return HttpResponse('You are not authorized to view and Create the New User please take the permission to the admin')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'account/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    brands = Brand.objects.all().order_by('-created')
    contents = Content.objects.all().order_by('-updated')
    total_content = contents.count()
    total_brand = brands.count()
    context = {
        'brands': brands,
        'contents': contents,
        'total_content': total_content,
        'total_brand': total_brand,
    }
    return render(request, 'account/home.html', context)


@login_required(login_url='login')
def brandPage(request):
    brands = Brand.objects.all().order_by('-created')
    total_brand = brands.count()
    myFilter = BrandFilter(request.GET, queryset=brands)
    contents = myFilter.qs
    context = {
        'brands': brands,
        'total_brand': total_brand,
        'brand': contents,
        'filter': myFilter,
    }
    return render(request, 'account/brand.html', context)



@login_required(login_url='login')
def contentPage(request):
    contents = Content.objects.all().order_by('-updated')
    total_content = contents.count()
    contentFilter = ContentFilter(request.GET, queryset=contents)
    contents = contentFilter.qs
    context = {
        'contents': contents,
        'total_content': total_content,
        'contentFilter': contentFilter,
    }
    return render(request, 'account/contentPage.html', context)



@login_required(login_url='login')
def single_brand(request, slug):
    brand = Brand.objects.get(slug=slug)
    contents = brand.content_set.all().order_by('-updated')
    content_count = contents.count()
    myFilter = ContentFilter(request.GET, queryset=contents)
    contents = myFilter.qs
    context = {
        'brand': brand,
        'contents': contents,
        'content_count': content_count,
        'myFilter': myFilter,
    }
    return render(request, 'account/content.html', context)


@login_required(login_url='login')
def createContent(request, slug):
    brand = Brand.objects.get(slug=slug)
    form = ContentForm()
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form,
               'brand': brand}
    return render(request, 'account/content_form.html', context)


@login_required(login_url='login')
def createBrand(request):
    form = BrandForm()
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'account/brand_form.html', context)


@login_required(login_url='login')
def updateContent(request, pk):
    content = Content.objects.get(id=pk)
    form = ContentForm(instance=content)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
        'item': content
    }
    return render(request, 'account/content_form.html', context)


@login_required(login_url='login')
def updateBrand(request, slug):
    brand = Brand.objects.get(slug=slug)
    form = BrandForm(instance=brand)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
        'item': brand
    }
    return render(request, 'account/brand_form.html', context)


@login_required(login_url='login')
def deleteContent(request, pk):
    if request.user.is_superuser:
        content = Content.objects.get(id=pk)
        if request.method == 'POST':
            content.delete()
            return redirect('home')
        context = {'item': content}
        return render(request, 'account/delete.html', context)
    return HttpResponse('You are not authorized to view and delete this Content please take the permission to the admin')


@login_required(login_url='login')
def deleteBrand(request, slug):
    if request.user.is_superuser:
        brand = Brand.objects.get(slug=slug)
        if request.method == 'POST':
            brand.delete()
            return redirect('home')
        context = {'item': brand}
        return render(request, 'account/delete_brand.html', context)
    return HttpResponse('You are not authorized to view and delete this Brand please take the permission to the admin')


class UserChartView(LoginRequiredMixin, DetailView):
    template_name = 'account/brand_detail.html'

    def get_object(self):
        pk = self.kwargs.get('brand_slug')
        return pk

    def get_context_data(self, **kwargs):
        context = super(UserChartView, self).get_context_data(**kwargs)
        brand = Brand.objects.get(slug=self.get_object())
        qs = brand.content_set.all()
        context["qs"] = qs
        return context

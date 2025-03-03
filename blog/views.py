from django.shortcuts import render, get_object_or_404, redirect
from .models import Page
from .forms import PageForm, SignUpForm
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def about(request):
    return render(request, 'blog/about.html')  

def home(request):
    return render(request, 'home.html', {'welcome_message': '¡Bienvenido a nuestro blog!'})

def pages(request):
    pages = Page.objects.all() 
    no_pages_message = "No hay páginas creadas aún." if not pages else None  
    return render(request, 'blog/pages_list.html', {'pages': pages, 'no_pages_message': no_pages_message})

def page_detail(request, pk):
    page = get_object_or_404(Page, pk=pk) 
    return render(request, 'blog/page_detail.html', {'page': page})

@login_required
def create_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            new_page = form.save(commit=False)
            new_page.author = request.user  
            new_page.save()
            return redirect('pages')  
    else:
        form = PageForm()
    return render(request, 'create_page.html', {'form': form})
def update_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('page_detail', pk=page.pk)
    else:
        form = PageForm(instance=page)
    return render(request, 'update_page.html', {'form': form})

@login_required
def delete_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        page.delete()
        return redirect('pages')  
    return render(request, 'blog/delete_page.html', {'page': page})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pages')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')  
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})
def logout_user(request):
    logout(request)
    return redirect('login')



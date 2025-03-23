from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm 
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Page, Profile
from .forms import PageForm, SignUpForm, UserEditForm, ProfileEditForm

# Página de "Acerca de"
def about(request):
    return render(request, 'blog/about.html')

# Página de inicio
def home(request):
    return render(request, 'home.html', {'welcome_message': '¡Bienvenido a nuestro blog!'})

# CBV para listar las páginas
class PageListView(ListView):
    model = Page
    template_name = 'blog/pages_list.html'
    context_object_name = 'pages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['pages']:
            context['no_pages_message'] = "No hay páginas creadas aún."
        return context

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/page_detail.html'
    context_object_name = 'page'

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'create_page.html'
    success_url = reverse_lazy('pages')

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)

class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    fields = ['title', 'content', 'image']
    form_class = PageForm
    template_name = 'blog/update_page.html'
    success_url = reverse_lazy('pages')

    def get_success_url(self):
        return reverse_lazy('page_detail', kwargs={'pk': self.object.pk})

class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = 'blog/delete_page.html'
    success_url = reverse_lazy('pages')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Crear el perfil vacío para el nuevo usuario
            Profile.objects.create(user=user)

            return redirect('home')  # O la vista a la que desees redirigir
    else:
        form = UserCreationForm()

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

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    # Verificar si el perfil del usuario existe, si no, crearlo
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirigir al perfil después de guardar
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDoneViewCustom(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView


# Vista de perfil del usuario
@login_required
def profile(request):
    # Verificamos si el usuario tiene un perfil
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)  # Crear el perfil si no existe
    return render(request, 'users/profile.html')

# Vista de edición de perfil
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile')  # Redirigir al perfil después de guardar

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

# Vista personalizada para el cambio de contraseña
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:password_change_done')

class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile  # Obtiene el perfil del usuario autenticado

# Vista para editar el perfil del usuario
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'users/edit_profile.html'
    context_object_name = 'profile'

    form_class = ProfileEditForm
    success_url = reverse_lazy('users:profile')  # Redirige a la vista de perfil

    def get_object(self):
        return self.request.user.profile  # Edita solo el perfil del usuario autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserEditForm(instance=self.request.user)  # Agrega el formulario de usuario
        return context

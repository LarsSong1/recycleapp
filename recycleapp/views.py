from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUser, UpdateProfile, RecyclingData, CardBoardForm
from django.utils.translation import activate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

from django.contrib.auth.decorators import login_required


# Create your views here.


# -------------------------------------------------------------

# Registro de usuarios
def registerView(request):
    activate('es')
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recycleapp:login')
    else: 
        form = CreateUser()
    return render(request, 'registerPage.html', {'form': form})

# Inicio de Sesion de usuarios
def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}')
                return redirect('recycleapp:dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')


    form = AuthenticationForm()   

    form.fields['username'].label = 'Nombre de usuario'
    form.fields['password'].label = 'Contraseña'
    return render(request, 'loginPage.html', {"form": form})

def logoutApp(request):
    logout(request)
    return redirect('recycleapp:login')


# -------------------------------------------------------------



# -------------------------------------------------------------
# Crear un perfil por cada usuario creado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Guardar el perfil creado
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# -------------------------------------------------------------



# -------------------------------------------------------------
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_session = request.user
        context = {
            'users': users,
            'user_session': user_session
        }
        return render(request, 'dashboard.html', context)

# -------------------------------------------------------------




# -------------------------------------------------------------


def userProfile(request, pk):
    activate('es')
    user = get_object_or_404(User, pk=pk)
    myRecylcingData = RecyclingData.objects.filter(user=request.user)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('recycleapp:profile', pk=request.user.pk)
    else:
        form = UpdateProfile(instance=request.user)


    context = {
        'user': user,
        'form': form,
        'recyclingData': myRecylcingData
        
    }
    return render(request, 'profile.html', context)


# -------------------------------------------------------------




# -------------------------------------------------------------

# Carton
class RecycleView(View):
    activate('es')
    def get(self, request, *args, **kwargs):
        # Inicializa un formulario vacío para el GET
        recyclingDataForm = CardBoardForm()
        # Obtiene todos los datos existentes para mostrar
        recyclingDataList = RecyclingData.objects.all()
        context = {
            'form': recyclingDataForm,
            'data': recyclingDataList,  # Pasar un QuerySet para iterar en la plantilla
        }
        return render(request, 'recyclePage.html', context)

    def post(self, request, *args, **kwargs):
        # Manejo del formulario para guardar datos
        recyclingDataForm = CardBoardForm(request.POST)
        if recyclingDataForm.is_valid():
            recyclingDataForm.save()
            return redirect('recycleapp:profile', pk=request.user.id)  # Cambia esto por tu URL correspondiente

        # Si hay errores en el formulario, vuelve a renderizar la página con errores
        recyclingDataList = RecyclingData.objects.all()
        context = {
            'form': recyclingDataForm,
            'data': recyclingDataList,
        }
        return render(request, 'recyclePage.html', context)


# -------------------------------------------------------------
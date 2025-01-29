from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUser, UpdateProfile, RecyclingDataForm, RecyclingCenterForm
from django.utils.translation import activate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View, DeleteView
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile, RecyclingData, RecyclingCenter

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


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
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        data = RecyclingData.objects.all()
        user_session = request.user
        context = {
            'users': users,
            'user_session': user_session,
            'data': data
        }
        return render(request, 'dashboard.html', context)

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




def userProfile(request, pk):
    activate('es')
    user = get_object_or_404(User, pk=pk)
    myRecylcingData = RecyclingData.objects.filter(user=pk)
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

# Vista de reciclaje
class RecycleView(View):
    activate('es')
    def get(self, request, *args, **kwargs):
        # Inicializa un formulario vacío para el GET
        recyclingDataForm = RecyclingDataForm()
        # Obtiene todos los datos existentes para mostrar
        recyclingDataList = RecyclingData.objects.all()
        context = {
            'form': recyclingDataForm,
            'data': recyclingDataList,  # Pasar un QuerySet para iterar en la plantilla
        }
        return render(request, 'recyclePage.html', context)

    def post(self, request, *args, **kwargs):
        # Manejo del formulario para guardar datos
        recyclingDataForm = RecyclingDataForm(request.POST)
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



@login_required
def deleteRecyclingData(request, pk):
    recycling_data = get_object_or_404(RecyclingData, pk=pk)
    # Verifica que el registro pertenezca al usuario actual
    if recycling_data.user == request.user:
        recycling_data.delete()
        return redirect('recycleapp:profile', pk=request.user.pk)  # Redirige al perfil
    else:
        return HttpResponseForbidden("No tienes permiso para eliminar este registro.")



@login_required
def editRecyclingData(request, pk):
    recycling_data = get_object_or_404(RecyclingData, pk=pk)
    # Verifica que el registro pertenece al usuario actual
    if recycling_data.user != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este registro.")
    
    if request.method == 'POST':
        form = RecyclingDataForm(request.POST, instance=recycling_data)
        if form.is_valid():
            form.save()
            return redirect('recycleapp:profile', pk=request.user.pk)
    else:
        form = RecyclingDataForm(instance=recycling_data)

    context = {
        'form': form,
        'recycling_data': recycling_data,
    }
    return render(request, 'recyclePage.html', context)

# -------------------------------------------------------------



# Vista de Centros de reciclaje
# -------------------------------------------------------------


class RecycleCenterView(View):
    def get(self, request, *args, **kwargs):
        recycling_data = RecyclingData.objects.filter(user=request.user)
        recycling_centers = RecyclingCenter.objects.all()

        # Lista donde almacenaremos los cálculos para cada centro de reciclaje
        recycling_results = []

        for center in recycling_centers:
            center_data = {
                "center": center,
                "materials": []
            }
            
            for data in recycling_data:
                if data.density:  # Asegurar que la densidad está calculada
                    material_price = None
                    
                    if data.material == "Plástico":
                        material_price = data.density * center.plastic_price_per_kg
                    elif data.material == "Vidrio":
                        material_price = data.density * center.glass_price_per_kg
                    elif data.material == "Cartón":
                        material_price = data.density * center.cardboard_price_per_kg
                    
                    if material_price is not None:
                        center_data["materials"].append({
                            "material": data.material,
                            "density": round(data.density, 2),
                            "price": round(material_price, 2)
                        })
            
            recycling_results.append(center_data)

        context = {
            "recycling_results": recycling_results
        }

        return render(request, "recycleCenter.html", context)

    


class addReciclingCenter(View):
    def get(self, request, *args, **kwargs):
        recyclingCenter = RecyclingCenterForm()
        context = {
            'form': recyclingCenter,
            
        }
        return render(request, 'addRecycleCenter.html', context)
    
    def post(self, request, *args, **kwargs):
        
        # Manejo del formulario para guardar datos
        recyclingCenter = RecyclingCenterForm(request.POST)
        if recyclingCenter.is_valid():
            recyclingCenter.save()
            return redirect('recycleapp:dashboard')  # Cambia esto por tu URL correspondiente
        
        context = {
            'form': RecyclingCenter,
        }
        return render(request, 'addRecyclePage.html', context)
    






@login_required
def claim_material(request, material_id, center_id):
    """ Procesa el reclamo de un material y actualiza las ganancias del usuario. """
    material = get_object_or_404(RecyclingData, id=material_id, user=request.user)
    center = get_object_or_404(RecyclingCenter, id=center_id)

    if material.claimed:
        messages.error(request, "Este material ya ha sido reclamado.")
        return redirect('recycling_centers')  # Ajusta esto según tu URL de lista de centros

    # Obtener la ganancia en base a la densidad
    total_money = center.get_price_for_material(material.material, material.density)

    # Actualizar las ganancias del usuario
    if material.material == "Plástico":
        material.moneyPlastic += total_money
    elif material.material == "Vidrio":
        material.moneyGlass += total_money
    elif material.material == "Cartón":
        material.money_cardboard += total_money

    # Marcar como reclamado
    material.claimed = True
    material.save()

    messages.success(request, f"Material reclamado con éxito. Ganaste ${total_money:.2f}")
    return redirect('recycling_centers')  # Redirige de nuevo a la lista de centros


# -------------------------------------------------------------
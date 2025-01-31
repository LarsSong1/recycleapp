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
        data = RecyclingData.objects.filter(claimed=True)
        datauser = RecyclingData.objects.filter(claimed=True, user=request.user)
        moneyGlass = 0
        moneyCardBoard = 0
        moneyPlastic = 0
        for usersData in data:
            moneyGlass += usersData.moneyGlass
            moneyCardBoard += usersData.money_cardboard
            moneyPlastic += usersData.moneyPlastic

        cardboardRegister = sum(1 for d in data if d.material == 'Cartón')
        glassRegister = sum(1 for d in data if d.material == 'Vidrio')
        plasticRegister = sum(1 for d in data if d.material == 'Plástico')


        cardboardRegisterUser = sum(1 for d in datauser if d.material == 'Cartón')
        glassRegisterUser = sum(1 for d in datauser if d.material == 'Vidrio')
        plasticRegisterUser = sum(1 for d in datauser if d.material == 'Plástico')


        moneyPlastic = round(moneyPlastic, 2)
        moneyGlass = round(moneyGlass, 2)
        moneyCardBoard = round(moneyCardBoard, 2)   
         
 


        user_session = request.user
        context = {
            'users': users,
            'user_session': user_session,
            'data': data, 
            'glass': moneyGlass,
            'cardboard': moneyCardBoard,
            'plastic': moneyPlastic,
            'recolected': data,
            'plasticCount': plasticRegister,
            'glassCount': glassRegister,
            'cardboardCount': cardboardRegister,
            'plasticCountUser': plasticRegisterUser,
            'glassCountUser': glassRegisterUser,
            'cardboardCountUser': cardboardRegisterUser,
            'user_photo': request.user.profile.photo.url if request.user.profile.photo else None
           
            
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

    moneyCardBoard = 0
    moneyPlastic = 0
    moneyGlass = 0

    for data in RecyclingData.objects.filter(user=pk, claimed=True):
        moneyCardBoard += data.money_cardboard
        moneyPlastic += data.moneyPlastic
        moneyGlass += data.moneyGlass
        

    moneyCardBoard = round(moneyCardBoard, 2)
    moneyCardBoard = round(moneyCardBoard, 2)
    moneyGlass = round(moneyGlass, 2)



    print(moneyGlass)
    



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
        'recyclingData': myRecylcingData,
        'cardboard': moneyCardBoard,
        'plastic': moneyPlastic,
        'glass': moneyGlass,
        'user_photo': request.user.profile.photo.url if request.user.profile.photo else None

        
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
            recycling_data = recyclingDataForm.save(commit=False)
            recycling_data.user = request.user
            recycling_data.save()
            return redirect('recycleapp:profile', pk=request.user.pk)  # Cambia esto por tu URL correspondiente

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
                    
                    
                    if data.material == "Plástico":
                        material_price = round(float(data.density) * center.plastic_price_per_kg, 2)
                        
                       
                    
                    elif data.material == "Vidrio":
                       
                        material_price = round(float(data.density) * center.glass_price_per_kg, 2)
                    
                    
                    elif data.material == "Cartón":
                      
                        material_price = round(float(data.density) * center.cardboard_price_per_kg, 2)
                  
                    


                    
                    if material_price > 0:
                        center_data["materials"].append({
                            "material": data.material,
                            "density": round(data.density, 2),
                            "price": material_price,
                            "id": data.id, 
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
        return render(request, 'addRecycleCenter.html', context)
    





# Por Revisar

def claimMaterial(request, center_id):
    """ Procesa el reclamo de múltiples materiales y actualiza las ganancias del usuario. """
    center = get_object_or_404(RecyclingCenter, id=center_id)

    if request.method == 'POST':
        # Obtener todos los materiales seleccionados
        all_materials = RecyclingData.objects.filter(user=request.user, claimed=False)
        print("Todos los materiales del usuario:")
        for material in all_materials:
            print(f"Material: {material.material}, Densidad: {material.density}, Reclamado: {material.claimed}")



        if not all_materials:
            messages.error(request, "No hay materiales seleccionados o ya reclamados.")
            return redirect('recycleapp:recycle-center')  # Redirige si no se seleccionaron materiales

        total_money = 0

        # Procesa cada material seleccionado
        for material in all_materials:
            print(f"{material.material} - Densidad: {material.density} - Reclamado: {material.claimed}")
            material_price = center.get_price_for_material(material.material, material.density)
            total_money += material_price

            # Actualizar las ganancias del usuario en base al tipo de material
            if material.material == "Plástico":
                print(f"Antes: moneyPlastic = {material.moneyPlastic}")
                material.moneyPlastic += material_price
                print(f"Después: moneyPlastic = {material.moneyPlastic}")

            elif material.material == "Vidrio":
                print(f"Antes: moneyGlass = {material.moneyGlass}")
                material.moneyGlass += material_price
                print(f"Después: moneyGlass = {material.moneyGlass}")
              

            elif material.material == "Cartón":
                print(f"Antes: moneyCardboard = {material.money_cardboard}")
                material.money_cardboard += material_price
                print(f"Después: moneyCardboard = {material.money_cardboard}")
               

            # Marcar como reclamado
          
            material.claimed = True
            material.density = 0
            



            material.save(update_fields=['moneyPlastic', 'moneyGlass', 'money_cardboard', 'claimed', 'density'])

        messages.success(request, f"¡Has reclamado los materiales! Ganaste ${total_money:.2f}.")
        if request.user.is_authenticated and request.user.pk:
            return redirect('recycleapp:profile', pk=request.user.pk)  # Redirige después de reclamar todos los materiales
    else:
        # Redirige si no es un método POST
        return redirect('recycleapp:recycle-center')

# -------------------------------------------------------------
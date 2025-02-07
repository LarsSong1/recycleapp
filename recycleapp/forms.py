from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm

from .models import Profile, RecyclingData, RecyclingCenter




class CreateUser(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': _('Solo se aceptan letras o estos caracteres @/./+/-/_ '),
            'password2': _('Vuelve a ingresar la misma contraseña'),
            'password1': _('Tu contraseña no debe ser similar a tu usuario.\n'
                           'Debe contener al menos 8 caracteres\n'
                           'No uses contraseñas habituales\n'
                           'No debe ser solo numeros'),
        }




class UpdateProfile(UserChangeForm):
    photo = forms.ImageField(required=False, label=_('Foto de perfil'))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {
            'username': _('Solo se aceptan letras o estos caracteres @/./+/-/_ '),
            'password2': _('Vuelve a ingresar la misma contraseña'),
            'password1': _('Tu contraseña no debe ser similar a tu usuario.\n'
                           'Debe contener al menos 8 caracteres\n'
                           'No uses contraseñas habituales\n'
                           'No debe ser solo números'),
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        # Crear el perfil si no existe
        if not hasattr(user, 'profile'):
            profile = Profile(user=user)
            profile.save()
        else:
            profile = user.profile

        # Si la foto ha sido proporcionada, la actualizamos
        if 'photo' in self.cleaned_data:
            profile.photo = self.cleaned_data['photo']
            profile.save()

        if commit:
            user.save()

        return user
    


class RecyclingDataForm(forms.ModelForm):
    class Meta:
        model = RecyclingData
        fields = ['material', 'weight', 'volume', 'location', 'collector_name', 'notes']
        labels = {
            'material': 'Material',
            'weight': 'Peso',
            'volume': 'Volumen',
            'location': 'Ubicación',
            'collector_name': 'Nombre del recolector',
            'notes': 'Notas'
        }
        help_texts = {
            'weight': _('Solo se aceptan pesos'),
            'notes': _('Puedes agregar notas por cada reciclaje que hagas'),
            'collector_name': _('Tu nombre o el de la persona que realizó la recolección')
        }


class RecyclingCenterForm(forms.ModelForm):
    class Meta:
        model = RecyclingCenter
        fields = ['name', 'address', 'url_maps', 'contact_info', 'plastic_price_per_kg', 'glass_price_per_kg', 'cardboard_price_per_kg']
        labels = {
            'name': 'Nombre',
            'address': 'Dirección',
            'url_maps': 'Ubicación por Google Maps',
            'contact_info': 'Número de contacto',
            'plastic_price_per_kg': 'Precio del Plástico por KG',
            'glass_price_per_kg':  'Precio del Vidrio por KG',
            'cardboard_price_per_kg':  'Precio del Cartón por KG'
        }
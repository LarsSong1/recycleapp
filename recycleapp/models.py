from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class MaterialChoices(models.TextChoices):
    PLASTIC = 'Plástico', 'Plástico'
    GLASS = 'Vidrio', 'Vidrio'
    CARDBOARD = 'Cartón', 'Cartón'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)  # Carpeta donde se guardan las fotos

    def __str__(self):
        return f"Perfil de {self.user.username}"


class RecyclingData(models.Model):
    material = models.CharField(max_length=20, choices=MaterialChoices.choices)
    weight = models.FloatField()
    volume = models.FloatField()
    density = models.FloatField(blank=True, null=True)  # Densidad calculada (kg/m³)
    recolected = models.FloatField(blank=True, null=True)
    date_collected = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255)
    collector_name = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    claimed = models.BooleanField(default=False)
    money = models.FloatField(default=0)
    money_cardboard = models.FloatField(default=0)
    moneyGlass = models.FloatField(default=0)
    moneyPlastic = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    

    def __str__(self):
        return f"{self.material} - {self.weight}kg - {self.volume}m³"
    

    def calculate_density(self):
        """
        Calcula la densidad usando la fórmula: Densidad = Peso / Volumen.
        Si el volumen es 0, se devuelve None para evitar divisiones por cero.
        """
        if self.volume > 0:
            return self.weight / self.volume
        return None
    
    def save(self, *args, **kwargs):
        """
        Calcula la densidad antes de guardar si hay peso y volumen válidos.
        """
        # if self.weight and self.volume:
        #     self.density = self.calculate_density()
        # super().save(*args, **kwargs)

        if self.claimed:
            self.density = 0  # Si el material ya fue reclamado, la densidad se pone en 0.
        elif self.weight and self.volume:
            self.density = self.calculate_density()
            self.recolected = self.calculate_density()

        super().save(*args, **kwargs)
        
        

    





class RecyclingCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    url_maps = models.URLField(max_length=1000, blank=False, null=False)
    contact_info = models.CharField(max_length=100, null=True, blank=True)
    plastic_price_per_kg = models.FloatField(blank=False, null=False)
    glass_price_per_kg = models.FloatField(blank=False, null=False)
    cardboard_price_per_kg = models.FloatField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_price_for_material(self, material, weight):
        """Calcula el precio total para un material dado y su peso."""
        if material == MaterialChoices.PLASTIC:
            return weight * self.plastic_price_per_kg
        elif material == MaterialChoices.GLASS:
            return weight * self.glass_price_per_kg
        elif material == MaterialChoices.CARDBOARD:
            return weight * self.cardboard_price_per_kg
        return 0.0




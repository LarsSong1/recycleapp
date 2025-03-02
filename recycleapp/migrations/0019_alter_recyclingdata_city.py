# Generated by Django 5.1.5 on 2025-02-10 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycleapp', '0018_alter_recyclingdata_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingdata',
            name='city',
            field=models.CharField(choices=[('Milagro', 'Milagro'), ('Cuenca', 'Cuenca'), ('Guaranda', 'Guaranda'), ('Azogues', 'Azogues'), ('Tulcán', 'Tulcán'), ('Riobamba', 'Riobamba'), ('Latacunga', 'Latacunga'), ('Machala', 'Machala'), ('Esmeraldas', 'Esmeraldas'), ('Puerto Baquerizo Moreno', 'Puerto Baquerizo Moreno'), ('Guayaquil', 'Guayaquil'), ('Ibarra', 'Ibarra'), ('Loja', 'Loja'), ('Babahoyo', 'Babahoyo'), ('Portoviejo', 'Portoviejo'), ('Macas', 'Macas'), ('Tena', 'Tena'), ('Puerto Francisco de Orellana', 'Puerto Francisco de Orellana'), ('Puyo', 'Puyo'), ('Quito', 'Quito'), ('Santa Elena', 'Santa Elena'), ('Santo Domingo', 'Santo Domingo'), ('Nueva Loja', 'Nueva Loja'), ('Ambato', 'Ambato'), ('Zamora', 'Zamora')], default='Sin Especificar', max_length=50),
        ),
    ]

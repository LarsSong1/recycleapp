# Generated by Django 5.1.5 on 2025-02-13 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycleapp', '0019_alter_recyclingdata_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingcenter',
            name='contact_info',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='recyclingdata',
            name='city',
            field=models.CharField(choices=[('Ambato', 'Ambato'), ('Azogues', 'Azogues'), ('Babahoyo', 'Babahoyo'), ('Cuenca', 'Cuenca'), ('Esmeraldas', 'Esmeraldas'), ('Guaranda', 'Guaranda'), ('Guayaquil', 'Guayaquil'), ('Ibarra', 'Ibarra'), ('Latacunga', 'Latacunga'), ('Loja', 'Loja'), ('Macas', 'Macas'), ('Machala', 'Machala'), ('Milagro', 'Milagro'), ('Nueva Loja', 'Nueva Loja'), ('Portoviejo', 'Portoviejo'), ('Puerto Baquerizo Moreno', 'Puerto Baquerizo Moreno'), ('Puerto Francisco de Orellana', 'Puerto Francisco de Orellana'), ('Puyo', 'Puyo'), ('Quito', 'Quito'), ('Riobamba', 'Riobamba'), ('Santa Elena', 'Santa Elena'), ('Santo Domingo', 'Santo Domingo'), ('Tena', 'Tena'), ('Tulcán', 'Tulcán'), ('Zamora', 'Zamora')], default='Sin Especificar', max_length=50),
        ),
        migrations.AlterField(
            model_name='recyclingdata',
            name='material',
            field=models.CharField(choices=[('Cartón', 'Cartón'), ('Vidrio', 'Vidrio'), ('Plástico', 'Plástico')], max_length=20),
        ),
        migrations.AlterField(
            model_name='recyclingdata',
            name='sector',
            field=models.CharField(choices=[('Centro', 'Centro'), ('Este', 'Este'), ('Norte', 'Norte'), ('Oeste', 'Oeste'), ('Rural', 'Rural'), ('Sur', 'Sur'), ('Urbano', 'Urbano')], default='Sin Especificar', max_length=50),
        ),
    ]

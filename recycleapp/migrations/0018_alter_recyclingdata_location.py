# Generated by Django 5.1.5 on 2025-02-10 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycleapp', '0017_recyclingdata_city_recyclingdata_province_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingdata',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-27 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycleapp', '0003_rename_user_id_recyclingdata_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingdata',
            name='date_collected',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

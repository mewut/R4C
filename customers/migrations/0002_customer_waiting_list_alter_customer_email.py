# Generated by Django 4.2.5 on 2023-09-29 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0002_robot_quantity'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='waiting_list',
            field=models.ManyToManyField(blank=True, related_name='waiting_list', to='robots.robot'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]

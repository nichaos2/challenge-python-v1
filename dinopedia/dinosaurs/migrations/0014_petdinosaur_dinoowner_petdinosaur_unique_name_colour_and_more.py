# Generated by Django 4.0.6 on 2022-07-25 11:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dinosaurs', '0013_delete_dinoowner'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetDinosaur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=250)),
                ('age', models.IntegerField()),
                ('height', models.FloatField(validators=[django.core.validators.MinValueValidator(0.001)])),
                ('length', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.001)])),
                ('width', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.001)])),
                ('weight', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.001)])),
                ('colour', models.CharField(max_length=250)),
                ('diet', models.CharField(max_length=250)),
                ('pet_description', models.TextField(null=True)),
                ('dino_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dinosaurs.dinosaur')),
            ],
            options={
                'ordering': ['pet_name'],
            },
        ),
        migrations.CreateModel(
            name='DinoOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='awesome dino owner', max_length=250)),
                ('liked_dinosaurs', models.ManyToManyField(to='dinosaurs.dinosaur')),
                ('petDino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dinosaurs.period')),
            ],
            options={
                'ordering': ['nickname'],
            },
        ),
        migrations.AddConstraint(
            model_name='petdinosaur',
            constraint=models.UniqueConstraint(fields=('pet_name', 'colour'), name='unique_name_colour'),
        ),
        migrations.AddConstraint(
            model_name='dinoowner',
            constraint=models.UniqueConstraint(fields=('nickname',), name='unique_owner_nickname'),
        ),
    ]

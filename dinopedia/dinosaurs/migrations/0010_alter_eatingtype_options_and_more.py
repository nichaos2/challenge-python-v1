# Generated by Django 4.0.6 on 2022-07-23 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dinosaurs', '0009_alter_period_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eatingtype',
            options={'ordering': ['eating_type']},
        ),
        migrations.RemoveConstraint(
            model_name='eatingtype',
            name='unique_eating_type',
        ),
        migrations.RenameField(
            model_name='dinosaur',
            old_name='eating',
            new_name='eating_type',
        ),
        migrations.RenameField(
            model_name='eatingtype',
            old_name='eating',
            new_name='eating_type',
        ),
        migrations.AddConstraint(
            model_name='eatingtype',
            constraint=models.UniqueConstraint(fields=('eating_type',), name='unique_eating_type'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-12 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_cliente_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=200, null=True, unique=True),
        ),
    ]
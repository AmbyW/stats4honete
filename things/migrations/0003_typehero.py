# Generated by Django 3.0 on 2020-04-19 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0002_typeteam'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeHero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True, verbose_name='Tipo de Héroe')),
                ('code', models.CharField(max_length=1, unique=True, verbose_name='Código')),
            ],
            options={
                'verbose_name': 'Tipo de Héroe',
                'verbose_name_plural': 'Tipos de Héroes',
            },
        ),
    ]
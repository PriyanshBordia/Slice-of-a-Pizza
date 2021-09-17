# Generated by Django 3.0.6 on 2020-05-15 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pasta', models.CharField(max_length=64)),
                ('Price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Regular_Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pizza', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Salads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Salad', models.CharField(max_length=64)),
                ('Price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Subs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Toppings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Topping', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Dinner_Platters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Platter', models.CharField(max_length=64)),
                ('Small', models.BooleanField(blank=True)),
                ('Large', models.BooleanField(blank=True)),
                ('Tops', models.ManyToManyField(related_name='topz', to='orders.Toppings')),
            ],
        ),
    ]
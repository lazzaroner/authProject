# Generated by Django 3.0.5 on 2020-04-13 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuyuadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=256),
        ),
    ]
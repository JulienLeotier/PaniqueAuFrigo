# Generated by Django 4.1.7 on 2023-02-24 15:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("perso", "0026_alter_secret_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="secret",
            name="description",
            field=models.CharField(max_length=3000),
        ),
    ]

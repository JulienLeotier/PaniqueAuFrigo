# Generated by Django 4.1.7 on 2023-02-22 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("perso", "0009_secret_perso"),
    ]

    operations = [
        migrations.AlterField(
            model_name="knownsecrets",
            name="description",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="knownsecrets",
            name="name",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="secret",
            name="description",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="secret",
            name="name",
            field=models.CharField(max_length=1000),
        ),
    ]

# Generated by Django 4.1.7 on 2023-02-22 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("perso", "0011_relation_perso_relations"),
    ]

    operations = [
        migrations.AddField(
            model_name="secret",
            name="image",
            field=models.ImageField(default="", upload_to="secret/images"),
        ),
    ]
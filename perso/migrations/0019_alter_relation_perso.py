# Generated by Django 4.1.7 on 2023-02-22 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("perso", "0018_alter_knownsecrets_perso"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relation",
            name="perso",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="perso.perso",
            ),
        ),
    ]

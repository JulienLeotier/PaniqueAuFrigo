# Generated by Django 4.1.7 on 2023-02-24 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("perso", "0023_perso_description_breve"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sandby",
            name="AskTalkPerso",
        ),
        migrations.AlterField(
            model_name="perso",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="NotifyTalk",
        ),
        migrations.DeleteModel(
            name="SandBy",
        ),
    ]

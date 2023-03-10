# Generated by Django 4.1.7 on 2023-02-24 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("perso", "0019_alter_relation_perso"),
    ]

    operations = [
        migrations.AlterField(
            model_name="savedocument",
            name="secrets",
            field=models.ManyToManyField(
                blank=True, related_name="save_secrets", to="perso.secret"
            ),
        ),
        migrations.CreateModel(
            name="SandBy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("validate", models.BooleanField(default=False)),
                (
                    "AskTalkPerso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="perso.asktalkperso",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotifyTalk",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "perso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="perso.perso"
                    ),
                ),
                (
                    "perso_ask",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="perso_ask_notify",
                        to="perso.perso",
                    ),
                ),
                (
                    "perso_join",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="perso_join_notify",
                        to="perso.perso",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

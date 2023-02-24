from django.contrib.auth.models import User
from django.db import models


# Perso model
# name: name of the character
# type: variety
# evidence: evidence of the character
# description: description of the character
# image: image of the character

class Perso(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="perso/images", default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    secrets = models.ManyToManyField("Secret", related_name="secrets", blank=True)
    known_secrets = models.ManyToManyField("KnownSecrets", related_name="known_secrets", blank=True)
    relations = models.ManyToManyField("Relation", related_name="relations", blank=True)
    saveDocument = models.ForeignKey("SaveDocument", on_delete=models.CASCADE, related_name="saveDocument", blank=True,
                                     null=True)
    slug_name = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description_breve = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GuiltyList(models.Model):
    guiltyPerso: Perso = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="guiltyPerso")
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="perso")

    def __str__(self):
        return self.perso.name


class Secret(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=3000)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="secret/images", default="", blank=True, null=True)

    def __str__(self):
        return self.name


class KnownSecrets(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=3000)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Relation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class SaveDocument(models.Model):
    name = models.CharField(max_length=200)
    secrets = models.ManyToManyField("Secret", related_name="save_secrets", blank=True)

    def __str__(self):
        return self.name


class SaveAsk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compte = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class AskTalkPerso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE)
    join_perso = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="join_perso", blank=True, null=True)
    perso_ask = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="perso_ask")

    def __str__(self):
        return self.user.username

class HistoryAskTalkPerso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE)
    join_perso = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="history_join_perso", blank=True, null=True)
    perso_ask = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="history_perso_ask")

    def __str__(self):
        return self.user.username


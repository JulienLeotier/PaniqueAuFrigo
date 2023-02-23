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
    evidence = models.ForeignKey("Evidence", on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="perso/images", default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secrets = models.ManyToManyField("Secret", related_name="secrets")
    known_secrets = models.ManyToManyField("KnownSecrets", related_name="known_secrets")
    relations = models.ManyToManyField("Relation", related_name="relations")
    saveDocument = models.ForeignKey("SaveDocument", on_delete=models.CASCADE, related_name="saveDocument", blank=True,
                                     null=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Evidence(models.Model):
    name = models.CharField(max_length=200)
    photos = models.ManyToManyField("Photo", related_name="evidence")

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(upload_to="evidence/images", default="")

    def __str__(self):
        return self.image.name


class GuiltyList(models.Model):
    guiltyPerso: Perso = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="guiltyPerso")
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="perso")

    def __str__(self):
        return self.perso.name


class Secret(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="secret/images", default="")

    def __str__(self):
        return self.name


class KnownSecrets(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Relation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class SaveDocument(models.Model):
    name = models.CharField(max_length=200)
    secrets = models.ManyToManyField("Secret", related_name="save_secrets", blank=True, null=True)

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


class NotifyTalk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    perso = models.ForeignKey("Perso", on_delete=models.CASCADE)
    perso_ask = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="perso_ask_notify")
    perso_join = models.ForeignKey("Perso", on_delete=models.CASCADE, related_name="perso_join_notify")

    def __str__(self):
        return self.user.username


class SandBy(models.Model):
    AskTalkPerso = models.ForeignKey("AskTalkPerso", on_delete=models.CASCADE)
    validate = models.BooleanField(default=False)

    def __str__(self):
        return self.AskTalkPerso.user.username

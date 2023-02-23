from django.contrib import admin

from perso.models import Perso, Type, Evidence, Photo, GuiltyList, Secret, KnownSecrets, Relation, SaveDocument, \
    AskTalkPerso, SaveAsk

admin.site.register(Perso)
admin.site.register(Type)
admin.site.register(Evidence)
admin.site.register(Photo)
admin.site.register(GuiltyList)
admin.site.register(Secret)
admin.site.register(KnownSecrets)
admin.site.register(Relation)
admin.site.register(SaveDocument)
admin.site.register(AskTalkPerso)
admin.site.register(SaveAsk)

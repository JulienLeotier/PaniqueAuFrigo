from django.contrib import admin

from perso.models import Perso, Type, GuiltyList, Secret, KnownSecrets, Relation, SaveDocument, \
    AskTalkPerso, SaveAsk, HistoryAskTalkPerso

admin.site.register(Perso)
admin.site.register(Type)
admin.site.register(GuiltyList)
admin.site.register(Secret)
admin.site.register(KnownSecrets)
admin.site.register(Relation)
admin.site.register(SaveDocument)
admin.site.register(AskTalkPerso)
admin.site.register(SaveAsk)
admin.site.register(HistoryAskTalkPerso);

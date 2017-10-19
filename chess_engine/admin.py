from django.contrib import admin
from .models import GamePersistentData, UserColorSet, UserRanking

admin.site.register(GamePersistentData)
admin.site.register(UserColorSet)
admin.site.register(UserRanking)

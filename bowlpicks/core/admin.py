from django.contrib import admin
from bowlpicks.core.models import Season, Conference, School, Team, Game, Pick
from bowlpicks.core import listeners


class GameAdmin(admin.ModelAdmin):
    list_filter = ('season__year_end', )
    list_display = (
        'name',
        'date',
        'season',
        'home_team',
        'home_score',
        'away_team',
        'away_score',)


class PickAdmin(admin.ModelAdmin):
    list_filter = ('player__name', 'game__season__year_end', 'game__name', )
    list_display = ('player', 'game', 'winner', )

admin.site.register(Season)
admin.site.register(Conference)
admin.site.register(School)
admin.site.register(Team)
admin.site.register(Game, GameAdmin)
admin.site.register(Pick, PickAdmin)

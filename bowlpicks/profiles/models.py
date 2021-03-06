from django.db import models
from django.db.models import get_model

from idios.models import ProfileBase


class Profile(ProfileBase):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        if self.first_name or self.last_name:
            return u"%s" % self.full_name
        else:
            return self.user.username

    def current_season(self):
        model = get_model('core', 'Season')
        return model.objects.current()


class Player(models.Model):
    profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=100, unique=True)
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    season = models.ManyToManyField('core.Season')

    def __unicode__(self):
        return u"%s" % self.name

    @property
    def points(self):
        points = 0
        for p in self.pick_set.curent_season():
            if p.correct:
                points += 1
        return points

    @property
    def wrong(self):
        count = 0
        for p in self.pick_set.curent_season():
            if not p.correct:
                count += 1
        return count

    def rank(self, season=None):
        if season is None:
            rankings = PlayerRanking.objects.current_season()
        else:
            rankings = PlayerRanking.objects.filter(season=season)
        count = 0
        for rank in rankings:
            count += 1
            if rank.player == self:
                return count
        return 'N/A'

    def current_active(self):
        model = models.get_model('core', 'Season')
        return self.active and self.season == model.objects.current()

    def current_player(self):
        model = models.get_model('core', 'Season')
        return model.objects.current() in self.season.all()


class PlayerRankingManager(models.Manager):

    def current_season(self):
        model = models.get_model('core', 'Season')
        return self.filter(season=model.objects.current())


class PlayerRanking(models.Model):
    season = models.ForeignKey('core.Season')
    player = models.ForeignKey(Player)
    correct = models.IntegerField(null=True)
    wrong = models.IntegerField(null=True)

    objects = PlayerRankingManager()

    class Meta:
        ordering = ('-correct', )

    def __unicode__(self):
        return "%s (%s)" % (self.player, self.season)

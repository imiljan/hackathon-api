from django.db import models
from django.contrib.auth.models import User


class Interest(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    color = models.CharField(max_length=128)

    def __str__(self):
        return 'Name {} '.format(self.name)


class Event(models.Model):
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField()
    img = models.ImageField(upload_to='static/images', max_length=255)
    address = models.CharField(max_length=128)
    hashtag = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.BooleanField(default=False)
    start_at = models.DateTimeField(null=False)  # TODO SETTINGS FOR DATETIME FORMAT AND INPUT
    end_at = models.DateTimeField(null=True)  # If null event is permanent
    lat = models.FloatField()
    long = models.FloatField()
    votes = models.ManyToManyField(User, through='Vote')
    interest = models.ForeignKey(Interest)

    def __str__(self):
        return 'Title {}'.format(self.title)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sign = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User {} voted for {}'.format(self.user, self.event)


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return 'User {} is interested in {}'.format(self.user, self.interest)


class UserCheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return 'User {} checked in {}'.format(self.user, self.event)

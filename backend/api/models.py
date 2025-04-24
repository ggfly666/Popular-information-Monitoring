from django.db import models

class CrawlTime(models.Model):
    Wbtime = models.IntegerField()
    Bdtime = models.IntegerField()
    Bltime = models.IntegerField()

    class Meta:
        db_table = 'CrawlTime'

class PushTime(models.Model):
    Wbtime = models.IntegerField()
    Bdtime = models.IntegerField()
    Bltime = models.IntegerField()

    class Meta:
        db_table = 'PushTime'

class Wb(models.Model):
    ranking = models.IntegerField()
    info = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    hot = models.CharField(max_length=255)
    uptime = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'Wb'

class Bd(models.Model):
    ranking = models.IntegerField()
    info = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    hot = models.CharField(max_length=255)
    uptime = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'Bd'

class Bl(models.Model):
    ranking = models.IntegerField()
    info = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    hot = models.CharField(max_length=255)
    uptime = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'Bl'


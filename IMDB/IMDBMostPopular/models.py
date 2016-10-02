from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Movie(models.Model):
    def __unicode__(self):
        return self.movie_title
    id = models.AutoField(primary_key=True, default=1)
    movie_title=models.CharField(max_length=200)
    movie_rating=models.CharField(max_length=200)
    movie_rating_count=models.IntegerField(default=0)
    movie_year=models.CharField(max_length=200)
    movie_image=models.CharField(max_length=200)
    movie_summary=models.TextField()
    movie_link=models.CharField(max_length=200)
    movie_count=models.IntegerField(default=0)

    
    

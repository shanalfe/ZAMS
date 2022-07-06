from django.db import models
from django.contrib.auth.models import AbstractUser

# to flush data from a table in django shell
# In [1]: from main.models import Links

# In [2]: Links.objects.all().delete()

# Create your models here.
class Likes(models.Model):
  id = models.IntegerField(primary_key=True)
  id_movie = models.IntegerField(default=-1)
  id_movie_tmdb = models.IntegerField(default=-1)
  id_member = models.IntegerField()

#import tablib
#from import_export import resources
#from main.models import Likes
#likes_resource = resources.modelresource_factory(model=Likes)()
#dataset=tablib.Dataset(header=['id_like','id_movie','id_movie_tmdb','id_member']).load(open('likes.csv').read())
#result = likes_resource.import_data(dataset, dry_run=False, raise_errors=True)

class Links(models.Model):
  id = models.IntegerField(primary_key=True) # id of movie in ml-latest
  id_imdb= models.IntegerField(default=1)
  id_tmdb = models.IntegerField(default=1)

#import tablib
#from import_export import resources
#from main.models import Links 
#likes_resource = resources.modelresource_factory(model=Links)()
#dataset=tablib.Dataset(header=['movieId','id_imdb','id_tmdb']).load(open('links.csv').read())
#result = likes_resource.import_data(dataset, dry_run=False, raise_errors=True)


# Probably not necessary !
class Member(models.Model):
  id = models.IntegerField(primary_key=True) # id of movie in ml-latest
  username = models.CharField(max_length=220)
  password = models.CharField(max_length=220)
  email = models.EmailField()

#import tablib
#from import_export import resources
#from main.models import Member 
#likes_resource = resources.modelresource_factory(model=Member)()
#dataset=tablib.Dataset(header=['id_member','username','password', 'email']).load(open('member.csv').read())
#result = likes_resource.import_data(dataset, dry_run=False, raise_errors=True)

class Movie(models.Model):
  id = models.IntegerField(primary_key=True) # id of movie in ml-latest
  title = models.CharField(max_length=220)
  genres = models.CharField(max_length=220)

#import tablib
#from import_export import resources
#from main.models import Movie 
#likes_resource = resources.modelresource_factory(model=Movie)()
#dataset=tablib.Dataset(header=['id_movie','title','genres']).load(open('movie.csv').read())
#result = likes_resource.import_data(dataset, dry_run=False, raise_errors=True)

class Note(models.Model):
  id = models.IntegerField(primary_key=True) # id of movie in ml-latest
  id_movie = models.IntegerField()
  note = models.IntegerField()
  id_member = models.IntegerField()

#import tablib
#from import_export import resources
#from main.models import Note 
#likes_resource = resources.modelresource_factory(model=Note)()
#dataset=tablib.Dataset(header=['id_note','id_movie','note', 'id_member']).load(open('note.csv').read())
#result = likes_resource.import_data(dataset, dry_run=False, raise_errors=True)

class View(models.Model):
  id = models.IntegerField(primary_key=True) # id of movie in ml-latest
  id_movie = models.IntegerField()
  id_member = models.IntegerField()

#import tablib
#from import_export import resources
#from main.models import View 
#likes_resource = resources.modelresource_factory(model=View)()
#dataset=tablib.Dataset(header=['id_view','id_movie','id_member']).load(open('view.csv').read())
#result = likes_resource.import_data(dataset, dry_run=False, raise_errors=True)

class CustomUser(AbstractUser):
	pass

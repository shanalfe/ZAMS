# Django
from django.shortcuts import render
from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.contrib.auth import get_user_model, login, logout, authenticate
from .models import *
from .forms import *
import random

# Pandas - Algo
import pandas as pd
# TMDB 
import tmdbsimple

from tmdbv3api import TMDb, Genre, Discover
from tmdbv3api import Movie as tmdbMovie
from tmdbv3api import Person as tmdbPerson

tmdb = TMDb()
tmdbsimple.API_KEY = '705d2ebb10a757764e8093f3150f1a19'
tmdb.api_key = "705d2ebb10a757764e8093f3150f1a19"


# Models objetcs imports
User = get_user_model()
###############################################################
#########               POUR TOI ALEXIS               #########
###############################################################
def login_user(request):
  context = {} # Ceci doit rester vide pour cette page
  if request.method =="POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request,user)
      return redirect('index')

  return render(request, 'main/login.html', context)

def logout_user(request):
  context = {} # Ceci doit rester vide pour cette page
  logout(request)
  return redirect('index')

###############################################################
#########               POUR TOI ALEXIS               #########
###############################################################

def register(request):
  context = {} # Ceci doit rester vide pour cette page
  if request.method == "POST":
    form = RegisterForm(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    User.objects.create_user(username=username,
                            password=password,
                            email=email)
    user = authenticate(request, username=username, password=password)
    login(request, user)
    return redirect('index')
  return render(request, 'main/register.html', context)


def index(request):
  # 9 films
  movies = tmdbMovie().popular()[:16]

  popular_movies = movies[:6]
  carou_movies = movies[6:]
  context = {
    'index_movies' : popular_movies, # tableau de dictionnaire. utilisation index_movies[0].original_title
    'carousel' : carou_movies,
    'carousel_active' : carou_movies[0]
  }

  if request.method == "POST":
    print()
    if((request.POST.get("search_string") != None) and (request.POST.get("search") != None)):
      search_string = request.POST.get("search_string")
      return redirect('search/'+search_string)
  else:
    return render(request, 'main/index.html', context)

def getCredits(film_id):
  movie_crew = tmdbMovie().credits(film_id)
  persons = [] 
  for person in movie_crew['crew']:
    if person.job == "Director":
      update = {
        'job' : person.job,
        'photo' : person.profile_path,
        'id' : person.id,
        'name' : person.name
      }
      persons.append(update)
  i = 0
  for person in movie_crew['cast']:
      if i < 4: 
        update = {
          'job' : 'actor',
          'photo' : person.profile_path,
          'id' : person.id,
          'name' : person.name
        }
        persons.append(update)
        i += 1

  return persons

def fiche(request, film_id):
  if(request.method == "POST" and request.POST.get("search_string") != None and request.POST.get("search") != None):
    search_string = request.POST.get("search_string")
    return redirect('/main/search/'+search_string)
  else:
    movie = tmdbMovie().details(film_id)
    is_movie_already_liked = False
    if request.method == "POST":
      if request.user.is_authenticated:
        if request.POST.get("unlike") == None:
          if not is_movie_already_liked:
            Likes.objects.create(id_movie_tmdb=film_id, id_member=request.user.id)
        else:
          Likes.objects.filter(id_movie_tmdb=film_id, id_member=request.user.id).delete()
    movie_liked = Likes.objects.filter(id_member=request.user.id)
    for film in movie_liked:
      if film.id_movie_tmdb == film_id:
        is_movie_already_liked = True
    credits = getCredits(film_id) 
    director = {}
    actors = []
    for credit in credits:
      if credit['job'] == 'Director':
        director = credit
      else:
        actors.append(credit) 
    print(is_movie_already_liked)
    stars_filled = int(movie.vote_average)
    stars_empty = 10 - stars_filled 
    context = {
      'movie' : movie,
      'liked' : is_movie_already_liked,
      'director' : director,
      'actors' : actors,
      'stars_filled' : range(stars_filled),
      'stars_empty' : range(stars_empty)
    }
    return render(request, 'main/fiche.html', context)

def films(request):
  ##### BASE VALUES #####
  genres = Genre().movie_list()
  genres.insert(0,{'id':0,'name':"All"})
  filtres = [{'val': "popularity", 'name':"Popularité"},
             {'val': "release_date", 'name':"Date de sortie"},
             {'val': "original_title", 'name':"Titre"},
             {'val': "vote_average", 'name':"Note"}]
  asc = False
  tri = "desc"
  filtre = "popularity"
  oldFiltre = "popularity"
  newGenre = 0
  oldGenre = 0
  maxPages=10
  page = 1
  maxPages = 1234

  # Récupération puis changement du tri

  if request.method == "POST":
    if request.POST.get("search_string") != None and request.POST.get("search") != None:
      search_string = request.POST.get("search_string")
      return redirect('/main/search/'+search_string)
    else:
      ##### TRI #####
      if(request.POST.get("sensTriActuel") != None):
        tri = request.POST.get("sensTriActuel")
        if(tri=="asc"):
          asc = True
        else:
          asc = False

      if(request.POST.get("tri") != None):
        tri = request.POST.get("tri")
        if(tri=="asc"):
          tri = "desc"
          asc = False
        else:
          tri = "asc"
          asc = True

      ##### PAGE #####
      if(request.POST.get("pageActuelle") != None):
        page = int(request.POST.get("pageActuelle"))
      if(request.POST.get("maxPages") != None):
        maxPages = int(request.POST.get("maxPages"))

      if(request.POST.get("previousPage") != None):
        if(page>1):
          page-=1
      elif(request.POST.get("nextPage") != None):
        if(page < maxPages):
          page+=1

      ##### FILTRES #####
      if(request.POST.get("filtreActuel") != None):
        oldFiltre = request.POST.get("filtreActuel")
      filtre = request.POST.get("sort_by")
      if(oldFiltre != filtre):
        page=1

      ##### GENRES #####
      if(request.POST.get("genreAcutel") != None):
        oldGenre = int(request.POST.get("genreAcutel"))
      newGenre = int(request.POST.get("with_genres"))
      if(oldGenre != newGenre):
        page=1
      rqGenre = newGenre
      if(newGenre==0):
        rqGenre=''

      ##### MOVIES #####
      tmdbResult = tmdbsimple.Discover().movie(
        include_adult = 'false',
        sort_by = filtre+'.'+tri, 
        page = page,
        with_genres = rqGenre
        )
      maxPages = tmdbResult["total_pages"]
      movies = tmdbResult["results"]
  else:
    tmdbResult = tmdbsimple.Movies().popular(include_adult = 'false')
    page = 1
    maxPages = tmdbResult["total_pages"]
    movies = tmdbResult["results"]

  for movie in movies :
    stars_filled = int(movie["vote_average"])
    stars_empty = 10 - stars_filled
    movie["stars_filled"] = range(stars_filled)
    movie["stars_empty"] = range(stars_empty)

  context = {
    'genres' : genres,
    'genre' : newGenre,
    'asc' : asc,
    'sensTriActuel':tri,
    'filtre' : filtre,
    'filtres': filtres,
    'movies' : movies,
    'pageActuelle' : page,
    'maxPages' : maxPages
  }
  return render(request, 'main/films.html', context)


def recommandation(request):
  if(request.method == "POST" and request.POST.get("search_string") != None and request.POST.get("search") != None):
    search_string = request.POST.get("search_string")
    return redirect('/main/search/'+search_string)
  else:
    recommended_movie = {} 
    if not request.user.is_authenticated:
      recommended_movie = tmdbMovie().popular()
      rand = random.randint(0,19)
      recommended_movie = recommended_movie[rand]
      pass
    else:
      # Get member
      member = get_object_or_404(User, pk=request.user.id)
      
      # Get his fav movies
      movie_liked = Likes.objects.filter(id_member=request.user.id) 
      for movie in movie_liked:
        #print(movie.id)
        pass
      
      if len(movie_liked) == 0:
        return render(request, 'main/index.html')

        # Get fav movies genre
          # Get fav movies tmdbId
      movie_liked_tmdbId = [] 
      for index in range(len(movie_liked)):
        if movie_liked[index].id_movie != -1:
          movie_liked_tmdbId.append(Links.objects.get(id=movie_liked[index].id).id_tmdb)
          #print(f"{movie_liked[index].id} and its ml id {movie_liked_tmdbId[index]}")
          pass
        else:
          movie_liked_tmdbId.append(movie_liked[index].id_movie_tmdb)
        pass
          # Get genres of favorite movies
      movie_liked_genres = []
      for index in range(len(movie_liked_tmdbId)):
        movie = tmdbMovie()
        movie_liked_genres.append(movie.details(movie_liked_tmdbId[index]).genres)
        #print(f"{movie_liked_genres[index]}")
        pass

      genres_dict = dict()
      for dict_ in movie_liked_genres:
        for item in dict_:
          dict_member = {
            item.id : {
              'value' : 1,
              'name' : item.name
            }
          }
          if item.id in genres_dict:
            genres_dict.update(dict_member)
          else:
            genres_dict.update(dict_member)
          pass
        #print(genres_dict)
      
      max_value = 0
      most_popular_genre = {} 
      for genre in genres_dict:
        if genres_dict[genre]['value'] > max_value:
            max_value = genres_dict[genre]['value']
            most_popular_genre = {
              'id' : genre,
              'name' : genres_dict[genre]['name'],
              'value' : max_value 
            } 
      #print(genres_dict)

      #######
      # SOME GENRES ARE NOT THE SAME BETWEEN tmdb and ML
      # BEWARE
      # For example Sci-Fi in ml and Science Fiction in tmdb 
      #######
      # Get movies of same genre
      # print(most_popular_genre)

      movies_of_same_genre = Movie.objects.filter(genres__icontains=f"{most_popular_genre['name']}")[:50] # I only take 50 movies
      movies_of_same_genre_tmdbId = [] 
      for index in range(len(movies_of_same_genre)):
        movies_of_same_genre_tmdbId.append(Links.objects.get(id=movies_of_same_genre[index].id).id_tmdb)
        #print(f"{movies_of_same_genre[index].id} and its tmdb id {movies_of_same_genre_tmdbId[index]}")
        pass

          # Get ratings of movie of same genre
      movies_of_same_genre_tmdb = {} 
      for index in range(len(movies_of_same_genre_tmdbId)):
        movie = tmdbMovie()
        movie = movie.details(movies_of_same_genre_tmdbId[index])
        rating = {
          movies_of_same_genre_tmdbId[index] : movie.vote_average
        }
        movies_of_same_genre_tmdb.update(rating)
        # print(f"{movies_of_same_genre_tmdb}")
        pass

      id_of_max_rating = 0
      max_rating = 0
      for item in movies_of_same_genre_tmdb:
        if movies_of_same_genre_tmdb[item] > max_rating:
          id_of_max_rating = item 
          max_rating = tmdbMovie().details(id_of_max_rating).vote_average

      recommended_movie = tmdbMovie().details(id_of_max_rating)
    #print(recommended_movie)

    credits = getCredits(recommended_movie.id) 
    director = {}
    actors = []
    for credit in credits:
      if credit['job'] == 'Director':
        director = credit
      else:
        actors.append(credit) 
    stars_filled = int(recommended_movie.vote_average)
    stars_empty = 10 - stars_filled 
    is_movie_already_liked = False
    if request.method == "POST":
      if request.user.is_authenticated:
        if request.POST.get("unlike") == None:
          if not is_movie_already_liked:
            Likes.objects.create(id_movie_tmdb=recommended_movie.id, id_member=request.user.id)
        else:
          Likes.objects.filter(id_movie_tmdb=recommended_movie.id, id_member=request.user.id).delete()
    movie_liked = Likes.objects.filter(id_member=request.user.id)
    for film in movie_liked:
      if film.id_movie_tmdb == recommended_movie.id:
        is_movie_already_liked = True
    context = {
      'movie' : recommended_movie,
      'liked' : is_movie_already_liked,
      'director' : director,
      'actors' : actors,
      'stars_filled' : range(stars_filled),
      'stars_empty' : range(stars_empty)
    }
    return render(request, 'main/fiche.html', context)

def like_test(request, film_id):
  movie = tmdbMovie().details(film_id)
  if request.method == "POST":
    if request.user.is_authenticated:
      Likes.objects.create(id_movie_tmdb=film_id, id_member=request.user.id)
  context = {
    'movie' : movie
  }
  return render(request, 'main/like_test.html', context)

def mesFilms(request):
  context = {}
  if request.user.is_authenticated:
    movie_liked = Likes.objects.filter(id_member=request.user.id)
    if len(movie_liked) == 0: # si pas de films likes n'affiche rien
      context = {}
      return(request, 'main/index.html', context)
    movies = []
    for movie in movie_liked:
      id = 0
      if movie.id_movie_tmdb == -1:
        id = Links.objects.get(id=movie.id_movie).id_tmdb
        movies.append(id)
      else:
        movies.append(movie.id_movie_tmdb)
      ### 
      # Remplir ici Maxime
      # movies est un tableau contenant les id_tmdb des films vu par l'user
      ###
    moviesToSend = []
    for film in movies :
      details = tmdbMovie().details(movie_id=film)
      moviesToSend.append(details)

    for film in moviesToSend :
      stars_filled = int(film["vote_average"])
      stars_empty = 10 - stars_filled
      film["stars_filled"] = range(stars_filled)
      film["stars_empty"] = range(stars_empty)

    print(moviesToSend)
    print(len(moviesToSend))
    context={
      'movies' : moviesToSend
    }
    return render(request, 'main/mesFilms.html', context)
  else:
    return (request, 'main/index.html', context)

def search(request, search_string):
  if(request.method == "POST" and request.POST.get("search_string") != None and request.POST.get("search") != None):
    search_string = request.POST.get("search_string")
    return redirect('/main/search/'+search_string)
  else:
    ##### BASE VALUES #####
    page = 1
    maxPages = 1234

    # Récupération puis changement du tri
      ##### PAGE #####
    if(request.POST.get("pageActuelle") != None):
      page = int(request.POST.get("pageActuelle"))
    if(request.POST.get("maxPages") != None):
      maxPages = int(request.POST.get("maxPages"))

    if(request.POST.get("previousPage") != None):
      if(page>1):
          page-=1
    elif(request.POST.get("nextPage") != None):
      if(page < maxPages):
        page+=1

      ##### MOVIES #####
    tmdbResult = tmdbsimple.Search().movie(
      query = search_string,
      page = page
      )
    maxPages = tmdbResult["total_pages"]
    movies = tmdbResult["results"]

    for movie in movies :
      stars_filled = int(movie["vote_average"])
      stars_empty = 10 - stars_filled
      movie["stars_filled"] = range(stars_filled)
      movie["stars_empty"] = range(stars_empty)

    context = {
      'movies' : movies,
      'pageActuelle' : page,
      'maxPages' : maxPages
    }
    return render(request, 'main/search.html', context)

def person(request, person_id):
  if(request.method == "POST" and request.POST.get("search_string") != None and request.POST.get("search") != None):
    search_string = request.POST.get("search_string")
    return redirect('/main/search/'+search_string)
  else:
    person_details = tmdbPerson().details(person_id)
    context= {
      'person' : person_details
    }
    return render(request, 'main/person.html', context)

"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
"""
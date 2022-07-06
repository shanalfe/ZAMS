from django.urls import path

from . import views


urlpatterns = [
    # ex: /main/
    path('', views.index, name='index'),
    # ex: /login/
    path('login/', views.login_user, name='login'),
    # ex: /register/
    path('register/', views.register, name='register'),
    # ex: /logout/
    path('logout/', views.logout_user, name='logout'),
    # ex: /fiche/<film_id>
    path('fiche/<int:film_id>/', views.fiche, name='fiche'),
    # ex: /films/
    path('films/', views.films, name='films'),
    # ex: /recommandation/
    path('recommandation/', views.recommandation, name='recommandation'),
    # ex: /mesFilms/
    path('mesFilms/', views.mesFilms, name='mesFilms'),
    # ex: /recommandation_test/
    path('recommandation_test/', views.recommandation, name='recommandation_test'),
    # ex: /like_test/<film_id>
    path('like_test/<int:film_id>', views.like_test, name='like_test'),
    # ex: /search/<string>
    path('search/<search_string>/', views.search, name='search'),
    # ex: /person/<person_id>
    path('person/<int:person_id>/', views.person, name='person'),
]

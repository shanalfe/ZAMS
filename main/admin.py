from django.contrib import admin
# Register your models here.

from import_export import resources
from .models import * 


# Used for django-import-export
class LikesResource(resources.ModelResource):

    class Meta:
        model = Likes 
        import_id_fields = ('id',)
        fields = ('id', 'id_movie', 'id_member',)

class LinksResource(resources.ModelResource):

    class Meta:
        model = Links 
        import_id_fields = ('id',)
        fields = ('id', 'id_imdb', 'id_tmdb',)

class MemberResource(resources.ModelResource):

    class Meta:
        model = Member 
        import_id_fields = ('id',)
        fields = ('id', 'username', 'password', 'email')

class MovieResource(resources.ModelResource):

    class Meta:
        model = Movie 
        import_id_fields = ('id',)
        fields = ('id', 'title', 'genres',)

class NoteResource(resources.ModelResource):

    class Meta:
        model = Note 
        import_id_fields = ('id',)
        fields = ('id', 'id_movie', 'note', 'id_member', )

class ViewResource(resources.ModelResource):

    class Meta:
        model = View 
        import_id_fields = ('id',)
        fields = ('id', 'id_movie', 'id_member', )

admin.site.register(Likes)
admin.site.register(Links)
admin.site.register(Member)
admin.site.register(Movie)
admin.site.register(Note)
admin.site.register(View)
admin.site.register(CustomUser)

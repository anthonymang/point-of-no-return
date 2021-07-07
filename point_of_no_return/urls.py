from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('database/artist', views.add, name='add'),
    path('database/music/<uri>/', views.music_add, name='music_add'),
    path('database/music/finish/<form_uri>/', views.music_create, name='music_create'),
    path('database/artist/create/<uri>/', views.artist_create, name='artist_create'),
    path('music/<uri>/', views.music_show, name='music_show'),
    path('artist/<uri>/', views.artist_show, name='artist_show'),
    path('search/music/', views.search_music, name='search_filter'),
    path('tags/<slug>/', views.tag_show, name = 'tag'),

]

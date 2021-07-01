from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('add/', views.add, name='add'),
    path('artist/create/<uri>', views.artist_create, name='artist_create')
]

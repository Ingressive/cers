from django.urls import path
from .views import home, signup, process_listen, mapV, listV
urlpatterns = [
    path('', home, name='home'), # Homepagge route
    path('map/', mapV, name='map'), # MapView route
    path('reports/', listV, name='list'), # Reports route
    path('listener/',  process_listen, name='listen'), # Webhook listener
    path('signup/', signup, name='signup') # Signup Route
]
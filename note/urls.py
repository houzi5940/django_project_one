from django.urls import path
from . import views

urlpatterns = [
	#http://127.0.0.1:8000/<应用名>/<应用名>/
	path('add/',views.add_note),
    path('list/',views.list_note),

]

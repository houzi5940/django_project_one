from django.urls import path
from . import views

urlpatterns = [
	#http://127.0.0.1:8000/<应用名>/<应用名>/
	path('reg/',views.reg_view),
	path('login/',views.login_view),
	path('logout/',views.logout_view),
]

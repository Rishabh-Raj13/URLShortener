from django.urls import path
from . import views
app_name = "url"
urlpatterns = [
    path("", views.urlShort, name="home"),
    path("<str:slugs>",views.urlRedirect, name="redirect"),
    path('delete/<slug:slug>/', views.delete_url, name='delete'), 
]
from django.urls import path
from . import views
from .views import SportDetailView

app_name = 'sport_app'

urlpatterns = [
    path('', views.SportListView.as_view(), name='sport_list'),
    path('add/', views.add_sport, name='add_sport'),
    path('<int:sport_id>/edit/', views.edit_sport, name='edit_sport'),
    path('<int:sport_id>/delete/', views.delete_sport, name='delete_sport'),
    path('<int:pk>/', SportDetailView.as_view(), name='sport_detail'),

]
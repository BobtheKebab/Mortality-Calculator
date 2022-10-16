from django.urls import path

from . import views

urlpatterns = [
    # /calculator/
    path('', views.index, name='index'),
    # /calculator/results/
    path('results/', views.results, name='results')
]
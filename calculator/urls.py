from django.urls import path

from . import views

urlpatterns = [
    # /calculator/
    path('', views.index, name='index'),
    # /calculator/results/
    path('results/', views.results, name='results'),
    # /calculator/visualize/
    path('visualize/', views.visualize, name='visualize'),
    # /calculator/compare/
    path('compare/', views.compare, name='compare'),
    # /calculator/compareForm/
    path('compareForm/', views.compareForm, name='compareForm'),
    # /calculator/compareCity/
    path('compareCity/', views.compareCity, name='compareCity'),
    # /calculator/bib/
    path('bib/', views.bib, name='bib')
]
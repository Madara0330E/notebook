from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery', RedirectView.as_view(pattern_name='index', permanent=True)),
    path('show/<int:id>/', views.show, name='show'),
    path('create/', views.create, name='create'),
    path('edit/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('add_contact/<int:id>/', views.add_contact, name='add_contact'),
    path('add_relationship/<int:id>/', views.add_relationship, name='add_relationship'),
    path('templates/', views.templates_list, name='templates_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/delete/<int:id>/', views.template_delete, name='template_delete'),
]

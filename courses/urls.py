from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('<slug:course_slug>/unit/<int:unit_order>/', views.unit_detail, name='unit_detail'),
    path('<slug:course_slug>/unit/<int:unit_order>/atom/<int:atom_order>/', views.atom_detail, name='atom_detail'),
    path('atom/<int:atom_id>/complete/', views.complete_atom, name='complete_atom'),
] 
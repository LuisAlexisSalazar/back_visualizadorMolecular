from django.urls import include, re_path, path

from . import views

app_name = "alignment_app"

urlpatterns = [
    # *Apis del Nuevo Modelo de Negocio
    path('api/global/', views.GlobalView.as_view(), name='Global'),
    path('api/local/', views.LocalView.as_view(), name='Local'),
    path('api/star/', views.StarView.as_view(), name='Star'),
    path('api/nussinov/', views.NussinovView.as_view(), name='Nussinov'),
]

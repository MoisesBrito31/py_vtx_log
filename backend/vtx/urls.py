from django.urls import path
from .views import IndexView, online, nodes, Filtra

urlpatterns = [
    path('',IndexView.as_view(),name="index"),
    path('filtra/',Filtra.as_view(),name="filtra"),
    path('online/',online,name="online"),
    path('nodes/',nodes,name="nodes"),
]
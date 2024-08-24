from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name='home'),
    path("form/",create_form,name="create_form"),
    path("delete/<int:id>",delete,name='delete'),
    path("edit/<int:id>",edit,name='edit'),
    path("login/",log_in,name='log_in'),
    path('register/',register,name='register'),
    path('change/',change_password,name='change_password'),
    path('recycle/',recycle,name='recycle'),
    path('restore/<int:id>',restore,name='restore'),
    path('search/',search,name='search')
]
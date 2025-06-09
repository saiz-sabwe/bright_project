# ModuleCarte/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/agents/', views.api_liste_agents, name='api_agents'),
    path('api/presences/', views.api_liste_presences, name='api_presences'),
    path('api/verifier-agent/<str:matricule>/', views.verifier_agent_par_matricule, name='verifier_agent'),

    path('api/enregistrer-presence/', views.enregistrer_presence, name='enregistrer_presence'),

]

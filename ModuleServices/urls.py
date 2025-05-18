from django.urls import path

from .views import ServiceListView, DemandeCreateView, DemandeListView, ProfessionnelByServiceView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list'),
    path('demandes/', DemandeCreateView.as_view(), name='demande-create'),
    path('demandes/mes/', DemandeListView.as_view(), name='demande-list'),
    path('professionnels/', ProfessionnelByServiceView.as_view(), name='professionnel-by-service'),

]

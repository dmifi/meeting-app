from django.urls import path

from users.views import RegistrationClientView, ClientDetailView, MatchListView, MatchDetailView, \
    ClientListView, SetMatch

urlpatterns = [
    path('api/clients/create', RegistrationClientView.as_view(), name='create'),
    path('api/clients', ClientListView.as_view(), name='clients_list'),
    path('api/clients/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('api/clients/<int:pk>/match', SetMatch.as_view(), name='client_match'),
    path('api/matches', MatchListView.as_view(), name='matches_list'),
    path('api/matches/<int:pk>', MatchDetailView.as_view(), name='matches_detail'),
]

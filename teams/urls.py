from django.urls import path

from teams.views import TeamView, TeamsDetailView

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<int:team_id>/", TeamsDetailView.as_view()),
]

from django.shortcuts import render
from datetime import datetime as dt
from rest_framework.views import APIView, Response, Request, status
from exceptions import NegativeTitlesError
from utils import data_processing
from .models import Team
from django.forms.models import model_to_dict


class TeamView(APIView):
    def get(self, req: Request) -> Response:
        teams = Team.objects.all()

        team_list = []

        for team in teams:
            team_dict = model_to_dict(team)
            team_list.append(team_dict)

        return Response(team_list, status.HTTP_200_OK)

    def post(self, req: Request) -> Response:
        first_world_cup = dt(1930, 1, 1)
        last_world_cup = dt(2022, 1, 1)
        date_first_cup = dt.strptime(req.data["first_cup"], "%Y-%m-%d")
        all_years_interval_last_first_cup = date_first_cup.year - first_world_cup.year
        all_cup_interval = (last_world_cup.year - date_first_cup.year) // 4

        print(date_first_cup.year)

        if req.data["titles"] < 0:
            return Response(
                {"error": "titles cannot be negative"}, status.HTTP_400_BAD_REQUEST
            )

        if (
            date_first_cup.year < first_world_cup.year
            or all_years_interval_last_first_cup % 4 != 0
        ):
            return Response(
                {"error": "there was no world cup this year"},
                status.HTTP_400_BAD_REQUEST,
            )

        if req.data["titles"] > all_cup_interval:
            return Response(
                {"error": "impossible to have more titles than disputed cups"},
                status.HTTP_400_BAD_REQUEST,
            )

        else:
            team = Team.objects.create(**req.data)
            team_dict = model_to_dict(team)
            return Response(team_dict, status.HTTP_201_CREATED)


class TeamsDetailView(APIView):
    def get(self, req: Request, team_id: int) -> Response:
        # team = Team.objects.get(id=team_id)

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not Found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)

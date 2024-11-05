from dataclasses import dataclass
from datetime import datetime

from dashboard.views.scoring import get_similarity_score
from django.urls import reverse
from ninja import Schema
from pydantic import Field
from repository.models import Constituency, UnlinkedConstituency
from repository.resolution.constituency import get_suggested_constituencies


class DashboardTaskNotificationSchema(Schema):
    title: str | None
    content: str | None
    complete: bool
    failed: bool
    created_on: datetime
    finished_at: datetime | None
    level: int


class DashboardMemberSchema(Schema):
    name: str
    url: str

    @staticmethod
    def resolve_url(obj):
        return reverse("admin:repository_person_change", args=[obj.pk])


class DashboardElectionSchema(Schema):
    name: str
    url: str
    date: datetime

    @staticmethod
    def resolve_url(obj):
        return reverse("admin:repository_election_change", args=[obj.pk])


class DashboardUnlinkedConstituencySchema(Schema):
    id: int
    name: str
    url: str
    person: DashboardMemberSchema
    election: DashboardElectionSchema

    @staticmethod
    def resolve_url(obj):
        return reverse("admin:repository_unlinkedconstituency_change", args=[obj.pk])


class ConstituencySuggestion(Schema):
    parliamentdotuk: int = Field(alias="constituency.parliamentdotuk")
    name: str = Field(alias="constituency.name")
    url: str
    start: datetime = Field(alias="constituency.start")
    end: datetime | None = Field(alias="constituency.end")
    score: int

    @staticmethod
    def resolve_url(obj):
        return reverse(
            "admin:repository_constituency_change", args=[obj.constituency.pk]
        )


@dataclass
class _ConstituencySuggestionWithScore:
    constituency: Constituency
    score: int


class DashboardUnlinkedConstituencyDetailSchema(Schema):
    suggestions: list[ConstituencySuggestion]

    @staticmethod
    def resolve_suggestions(obj: UnlinkedConstituency):
        _suggestions = get_suggested_constituencies(obj.name, obj.election.date)
        scored_suggestions = [
            _ConstituencySuggestionWithScore(
                constituency=constituency,
                score=get_similarity_score(obj.name, constituency.name),
            )
            for constituency in _suggestions
        ]

        return sorted(
            scored_suggestions,
            key=lambda s: s.score,
            reverse=True,
        )

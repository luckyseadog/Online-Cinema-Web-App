from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):

        table = Filmwork.objects.prefetch_related(
            "personfilmwork",
            "persons",
            'genres',
        ).annotate(
            Actors=ArrayAgg("persons__full_name", filter=Q(personfilmwork__role=PersonFilmwork.Role.ACTOR), distinct=True)
        ).annotate(
            Directors=ArrayAgg("persons__full_name", filter=Q(personfilmwork__role=PersonFilmwork.Role.DIRECTOR), distinct=True),
        ).annotate(
            Writers=ArrayAgg("persons__full_name", filter=Q(personfilmwork__role=PersonFilmwork.Role.WRITER), distinct=True),
        ).annotate(
            Genres=ArrayAgg('genres__name', distinct=True)
        ).values(
            "id", "title", "description", "creation_date", "rating", "type", "Genres", "Actors", "Directors", "Writers"
        )

        return table

    def render_to_response(self, context, **response_kwargs):
        if "results" in context:
            context["results"] = [{key.lower(): value  for key, value in d.items()} for d in context["results"]]
        else:
            context = {key.lower(): value for key, value in context.items()}
        return JsonResponse(context) 


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):

        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, 
            self.paginate_by
        )

        return {
            "count": paginator.count, 
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset)
        } 

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    
    def get_context_data(self, **kwargs):
        return self.object
        # return kwargs["object"]
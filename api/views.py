from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import Cast

from .models import Movie
from .serializer import MovieSerializer
from .validations import validate_query_params
from django.db.models import Q
from django.db.models import Case, When, IntegerField, Count

# Create your views here.

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    

    @action(detail=False, methods=['get'])
    def top(self, request):
        
        movies = self.queryset.order_by('-score')[:5]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    @validate_query_params
    def search(self, request):
        search = request.query_params.get('q') # search by q
        column = request.query_params.get('c', 'name') # sort by attribute
        sort = '' if request.query_params.get('o') == 'asc' else '-' # sort by asc or desc
        movies = self.queryset
        if search :
            movies = movies.filter(
                    Q(name__icontains=search) |
                    Q(country__icontains=search)
                )
        if column:
            
            movies = movies.order_by(sort + column)                
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)        
    @action(detail=False, methods=['get'])
    def summary(self, request):
        metric_countries = (self.queryset
            .values('country')
            .annotate(movies=Count('id'))
            .order_by()
        )
        metric_score = self.queryset.annotate(
            truncated_score=Cast('score', IntegerField())
        ).values('truncated_score').annotate(movies=Count('id')).order_by('truncated_score')
        
        return Response({'metric_country': metric_countries, 'metric_score' : metric_score})
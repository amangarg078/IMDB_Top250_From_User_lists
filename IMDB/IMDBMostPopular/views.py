from django.shortcuts import render ,get_object_or_404
from .models import Movie


def index(request):
    popular_movie_list=Movie.objects.order_by('-movie_count','-movie_rating_count')[:250]
    context={'popular_movie_list':popular_movie_list}
    return render(request,'IMDBMostPopular/index.html',context)


def movieDetails(request,id):
    movie=get_object_or_404(Movie,pk=id)
    return render(request,'IMDBMostPopular/details.html',{'movie':movie})



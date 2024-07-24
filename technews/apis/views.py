from django.shortcuts import render

# Create your views here.
# import viewsets
from rest_framework import viewsets

# import local data
from .serializers import NewsSerializer
from .models import NewsModel

# create a viewset


class NewsViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = NewsModel.objects.all()

	# specify serializer to be used
	serializer_class = NewsSerializer
	def get_queryset(self):
		queryset= super().get_queryset()
		tag = self.request.query_params.get('tag', None)
		if tag is not None:
			queryset = queryset.filter(tags__name=tag)
		return queryset

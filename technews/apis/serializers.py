# import serializer from rest_framework
from rest_framework import serializers

# import model from models.py
from .models import NewsModel, Tag

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ['id', 'name']
class NewsSerializer(serializers.HyperlinkedModelSerializer):
	tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
	class Meta:
		model = NewsModel
		fields = ('title', 'description', 'tags', 'source', )

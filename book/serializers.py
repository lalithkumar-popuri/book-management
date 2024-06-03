from rest_framework import serializers
from .models import BookModel
from django.contrib.auth.models import User

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class BookSerializer(serializers.HyperlinkedModelSerializer):
    author  = AuthorSerializer()
    class Meta:
        model = BookModel 
        fields = ["title","author","genre","description"]
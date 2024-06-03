from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import BookSerializer
from .models import BookModel

# Create your views here.


class CreateBookAPIView(CreateAPIView):
    serializer_class = BookSerializer
    queryset = BookModel.objects.all()
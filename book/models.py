from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class BookModel(models.Model):
    title = models.CharField(max_length=25)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    genre = models.CharField(max_length=25)
    publicationDate = models.DateField(auto_now=datetime.now)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title
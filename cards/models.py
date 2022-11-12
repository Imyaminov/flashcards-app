from django.db import models
from helpers.models import BaseModel

# Create your models here.

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES+1)

class Card(BaseModel):
    question = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    box = models.IntegerField(
        choices=BOXES,
        default=BOXES[0]
    )


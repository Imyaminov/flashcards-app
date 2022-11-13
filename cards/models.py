from django.db import models
from helpers.models import BaseModel

# Create your models here.

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES+1)

class Card(BaseModel):
    question = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0]
    )

    class Meta():
        ordering = ['box']

    def ___str__(self):
        return "{} - {}".format(self.question, self.answer)

    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]
        if new_box in BOXES:
            self.box = new_box
            self.save()
        return self



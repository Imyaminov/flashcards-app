from django.db import models
from helpers.models import BaseModel

# Create your models here.

NUM_BOXES = 5
BOXES = list(range(1, NUM_BOXES+1))

class Card(BaseModel):
    question = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0]
    )
    is_archive = models.BooleanField(
        verbose_name='Archive Card',
        default=False
    )

    class Meta():
        ordering = ['box']

    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]
        if new_box in BOXES[:len(BOXES)-1]:
            self.box = new_box
            self.save()
        return self

    def archive_unarchive_card(self):
        if not self.is_archive:
            self.is_archive = True
        elif self.is_archive:
            self.is_archive = False
        self.save()

    def __str__(self):
        return "{} - {}".format(self.question, self.answer)

# class Folder()
# class StudySet()
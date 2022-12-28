from django.db import models
from django.urls import reverse
from helpers.models import BaseModel
from common.models import CustomUser
# Create your models here.

NUM_BOXES = 5
BOXES = list(range(1, NUM_BOXES+1))

class Folder(BaseModel):
    title = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class StudySet(BaseModel):
    title = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    card_count = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_studyset')
    folder = models.ForeignKey(
        Folder,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='folder_studyset'
    )

    def cards_count(self):
        self.card_count = Card.objects.all().filter(study_set=self.pk).count()
        return self.card_count

    def studyset_cards(self):
        return Card.objects.all().filter(study_set=self.id)

    def save(self, *args, **kwargs):
        self.card_count = Card.objects.all().filter(study_set=self.pk).count()
        super(StudySet, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

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
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE, related_name='studyset')

    class Meta():
        ordering = ['box']

    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]
        print(new_box)
        if new_box in BOXES[:len(BOXES)]:
            self.box = new_box
            self.save()
        else:
            self.is_archive = True
            self.save()
        return self

    def archive_unarchive_card(self):
        if not self.is_archive:
            self.is_archive = True
        elif self.is_archive:
            self.is_archive = False
            self.box = BOXES[0]
        self.save()

    def __str__(self):
        return "{} - {}".format(self.question, self.answer)







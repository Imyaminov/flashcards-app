from django import template

from cards.models import BOXES, Card
from cards.views import get_user

register = template.Library()

@register.inclusion_tag('cards/box_link.html')
def boxes_as_links(username, **kwargs):
    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.all().filter(
            box=box_num,
            is_archive=False,
            study_set__author__username=username,
        )

        if kwargs['set']:
            card_count = card_count.filter(study_set=kwargs['set']).count()
        else:
            card_count = card_count.count()

        boxes.append({
            'number': box_num,
            'card_count': card_count,
            'study_set': kwargs['set'],
        })
    return {'boxes': boxes}
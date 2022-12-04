from django import template

from cards.models import BOXES, Card
from cards.views import get_user

register = template.Library()

@register.inclusion_tag('cards/box_link.html')
def boxes_as_links(username):
    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.all().filter(
            box=box_num,
            is_archive=False,
            study_set__author__username=username
        ).count()
        boxes.append({
            'number': box_num,
            'card_count': card_count,
        })
    return {'boxes': boxes}
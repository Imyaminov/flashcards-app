# Generated by Django 4.1.3 on 2022-12-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_alter_studyset_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyset',
            name='card_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

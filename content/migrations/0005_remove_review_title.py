# Generated by Django 3.1.7 on 2021-02-25 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_review_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
    ]
# Generated by Django 5.1.1 on 2024-09-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapeddata',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

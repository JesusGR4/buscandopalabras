# Generated by Django 2.2 on 2020-10-11 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_is_relevant'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_reviewed',
            field=models.BooleanField(default=False, help_text='Para referenciar su enlace dentro de otros artículos', verbose_name='Relevante'),
        ),
    ]
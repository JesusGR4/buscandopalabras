# Generated by Django 2.2 on 2020-10-12 20:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20201012_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, max_length=99999, null=True, verbose_name='Contenido'),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_reviewed',
            field=models.BooleanField(default=False, help_text='Para confirmar su revisión manual', verbose_name='Revisada'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Titulo'),
        ),
    ]

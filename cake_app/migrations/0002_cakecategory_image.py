# Generated by Django 4.1.7 on 2023-07-27 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cakecategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='изображение для категории'),
        ),
    ]

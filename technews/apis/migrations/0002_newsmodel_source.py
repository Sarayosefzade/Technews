# Generated by Django 4.2.14 on 2024-07-23 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsmodel',
            name='source',
            field=models.URLField(default='http://example.com'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0.2 on 2018-03-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappings',
            name='GEXF_LINK',
            field=models.TextField(default='NOGEXF'),
        ),
    ]

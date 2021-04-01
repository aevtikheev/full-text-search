# Generated by Django 3.1.7 on 2021-04-01 21:39

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20210401_2018'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='wine',
            name='desc_var_win_gin_idx',
        ),
        migrations.AddField(
            model_name='wine',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='wine',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='search_vector_gin_idx'),
        ),
    ]

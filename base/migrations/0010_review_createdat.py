# Generated by Django 3.2.5 on 2022-10-15 10:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_produst_review_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

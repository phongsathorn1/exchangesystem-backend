# Generated by Django 2.2.1 on 2019-05-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0011_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_avaliable',
            field=models.BooleanField(default=1),
        ),
    ]
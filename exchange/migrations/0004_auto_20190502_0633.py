# Generated by Django 2.2.1 on 2019-05-02 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20190501_1913'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('created_date',)},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='exchange.Category'),
            preserve_default=False,
        ),
    ]

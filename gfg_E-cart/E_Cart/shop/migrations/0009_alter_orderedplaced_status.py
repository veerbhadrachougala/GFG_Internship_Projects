# Generated by Django 4.2.2 on 2023-08-03 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_totalamount_orderedplaced_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedplaced',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('packed', 'packed'), ('Delivered', 'Delivered'), ('on the way', 'on the way'), ('canceled', 'canceled')], default='Accepted', max_length=50),
        ),
    ]
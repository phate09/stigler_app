# Generated by Django 3.1.2 on 2020-10-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0005_customer_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

# Generated by Django 4.2.17 on 2024-12-19 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_pass',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
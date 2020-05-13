# Generated by Django 3.0.5 on 2020-05-08 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(db_column='is_staff', default=False, error_messages={}, verbose_name='Is staff'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, db_column='date_joined', error_messages={}, verbose_name='Date joined'),
        ),
    ]

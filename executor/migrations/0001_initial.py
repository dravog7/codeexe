# Generated by Django 2.1 on 2018-08-15 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcases', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='submissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.BigIntegerField()),
                ('done', models.BooleanField()),
                ('subdate', models.DateTimeField()),
                ('lang', models.CharField(max_length=200)),
                ('code', models.TextField()),
                ('customin', models.TextField()),
                ('errors', models.TextField()),
                ('testresults', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='executor.questions')),
            ],
        ),
    ]

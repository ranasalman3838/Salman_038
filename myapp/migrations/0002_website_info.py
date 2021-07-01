# Generated by Django 3.2.3 on 2021-06-06 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_title', models.CharField(max_length=50)),
                ('website_copyright', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=50)),
                ('Contact', models.CharField(max_length=30)),
                ('Address', models.CharField(max_length=50)),
                ('Facebook', models.CharField(max_length=50)),
                ('Pintrest', models.CharField(max_length=50)),
                ('Instagram', models.CharField(max_length=50)),
                ('Twitter', models.CharField(max_length=50)),
            ],
        ),
    ]
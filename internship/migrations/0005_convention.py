# Generated by Django 2.2.2 on 2019-07-05 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0004_delete_convention'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=60)),
                ('life_time', models.IntegerField(default=0)),
                ('state', models.CharField(choices=[('R', 'Convention en cours'), ('S', 'Convention suspendue'), ('E', 'Convention expiree')], max_length=50)),
                ('starting_date', models.DateTimeField(auto_now_add=True)),
                ('enterprise', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='internship.Enterprise')),
            ],
        ),
    ]

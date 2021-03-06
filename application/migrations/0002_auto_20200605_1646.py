# Generated by Django 3.0.3 on 2020-06-05 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aliment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliment_id', models.IntegerField(null=True)),
                ('name', models.TextField()),
                ('category', models.TextField()),
                ('picture', models.TextField()),
                ('nutriscore', models.TextField()),
                ('description', models.TextField()),
                ('stores', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SavedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sauvegardé par')),
                ('saved_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Aliment', verbose_name='Produit sauvegardé')),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddConstraint(
            model_name='savedproduct',
            constraint=models.UniqueConstraint(fields=('saved_by', 'saved_product'), name='saved_association'),
        ),
    ]
